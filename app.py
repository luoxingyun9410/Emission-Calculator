from flask import Flask, render_template, request, redirect, url_for, jsonify, session, g, send_file
from collections import defaultdict
from io import StringIO, BytesIO
import sqlite3
import csv

app = Flask(__name__, template_folder='templates', static_folder='static')
app.secret_key = 'your_unique_secret_key'

emission_totals_global = {}

# Function to fetch all unique emission types from the database
def get_emission_types():
    conn = sqlite3.connect('emission_factors.db')
    cursor = conn.cursor()
    cursor.execute('SELECT DISTINCT emission_type FROM EmissionFactors')
    emission_types = [row[0] for row in cursor.fetchall()]
    conn.close()
    return emission_types

@app.route('/get_units', methods=['POST'])
def get_units():
    data = request.get_json()
    emission_type = data.get('emission_type')

    # Establish a connection to the SQLite database
    conn = sqlite3.connect('emission_factors.db')  # Ensure this is the correct path to your DB
    cursor = conn.cursor()

    # Fetch units for the selected emission type
    query = "SELECT DISTINCT unit FROM EmissionFactors WHERE emission_type = ?"
    units = [row[0] for row in cursor.execute(query, (emission_type,)).fetchall()]

    # Close the database connection
    conn.close()

    return jsonify(units)

# Route to render the main form
@app.route('/')
def index():
    emission_types = get_emission_types()  # Fetch emission types dynamically
    return render_template('index.html', emission_types=emission_types)

# API route to fetch units based on the emission type selected by the user
@app.route('/get_units', methods=['POST'])
def get_units_for_type():
    emission_type = request.json.get('emission_type')
    units = get_units(emission_type)
    return jsonify(units)

# Function to calculate emissions
@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        # Fetch the form data
        emission_type = request.form['emission_type']
        unit = request.form['unit']
        volume = float(request.form['volume'])

        # Connect to the database
        conn = sqlite3.connect('emission_factors.db')
        cursor = conn.cursor()

        # Query the emission factor and energy content
        cursor.execute('''
            SELECT emission_factor, energy_content
            FROM EmissionFactors
            WHERE emission_type = ? AND unit = ?
        ''', (emission_type, unit))

        # Fetch result from the database
        result = cursor.fetchone()

        # Close the database connection
        conn.close()

        if result:
            emission_factor, energy_content = result

            # Handle None energy_content case
            if emission_factor is None:
                emission_factor = 1  # Default value or adjust as needed

            # Perform the emissions calculation
            emissions = (volume * energy_content * emission_factor) / 1000

            # Render the results template with calculated data
            return render_template(
                'results.html',
                emission_type=emission_type,
                emissions=emissions,
                volume=volume,
                emission_factor=emission_factor,
                energy_content=energy_content
            )
        else:
            return "Error: Data not found for the selected emission type and unit", 400

    except ValueError:
        # Handle case where volume is not a valid float
        return "Error: Invalid input for volume. Please enter a valid number.", 400

    except Exception as e:
        # Catch all other exceptions and return an error message
        return f"Error: {str(e)}", 500



@app.route('/results', methods=['POST'])
def results():
    # Assume the emissions have been calculated here
    emission_type = request.form.get('emission_type', 'Bituminous coal')
    emissions = 90.24  # Example value
    
    return render_template('results.html',
                           emission_type=emission_type,
                           emissions=emissions,
                           volume=100,  # Example values
                           emission_factor=90.24,
                           energy_content=27)

@app.route('/summary', methods=['POST'])
def summary():
    # Retrieve the emission data from the form
    emission_type = request.form['emission_type']
    emissions = float(request.form['emissions'])
    volume = request.form.get('volume', 'N/A')
    emission_factor = request.form.get('emission_factor', 'N/A')
    energy_content = request.form.get('energy_content', 'N/A')

    # Initialize the total_emissions and emission details in session if not already set
    if 'total_emissions' not in session:
        session['total_emissions'] = 0.0
    if 'emission_details' not in session:
        session['emission_details'] = []

    # Add the current emissions to the total and round to two decimal places
    session['total_emissions'] = round(session['total_emissions'] + emissions, 2)
    total_emissions = session['total_emissions']

    # Store details of the calculation, rounding the emissions
    session['emission_details'].append({
        'emission_type': emission_type,
        'emissions': round(emissions, 2),
        'volume': volume,
        'emission_factor': emission_factor,
        'energy_content': energy_content,
        'formula': f"Emissions (t CO2-e) = ({volume} × {energy_content} × {emission_factor}) / 1000"
    })

    # Pass the details to the summary page
    return render_template('summary.html',
                           total_emissions=total_emissions,
                           emission_details=session['emission_details'])




@app.route('/')
def home():
    # If it's the first time, initialize the session variable
    if 'emission_history' not in session:
        session['emission_history'] = []  # Start with an empty list

    # Sum all previous calculations
    accumulated_emissions = sum(session['emission_history']) if session['emission_history'] else 0

    # Render the summary page with the accumulated total
    return render_template('summary.html', total_emissions=accumulated_emissions, emission_breakdown=[])

@app.route('/add_calculation', methods=['POST'])
def add_calculation():
    # Get the newly calculated emission value from the request
    new_emission = request.json.get('new_emission')

    # Append the new value to the session emission history
    session['emission_history'].append(new_emission)

    # Respond with the updated total emissions
    return jsonify({'status': 'success', 'total_emissions': sum(session['emission_history'])})

@app.route('/clear', methods=['POST'])
def clear_emissions():
    # Clear the total emissions and the emission details list
    session['total_emissions'] = 0.0
    session['emission_details'] = []
    return jsonify({'status': 'success'})  # Respond to the AJAX request

@app.route('/export_csv', methods=['GET'])
def export_csv():
    # Check if there are emission details to export
    emission_details = session.get('emission_details', [])
    if not emission_details:
        return jsonify({'status': 'error', 'message': 'No data to export'}), 400

    # Create a CSV file in memory using StringIO
    si = StringIO()
    writer = csv.writer(si)

    # Write the header without the "Formula" column
    writer.writerow(['Type', 'Emissions (t CO2-e)', 'Volume', 'Emission Factor', 'Energy Content'])

    # Write the data rows without the "Formula" column
    for detail in emission_details:
        writer.writerow([
            detail['emission_type'],
            detail['emissions'],
            detail['volume'],
            detail['emission_factor'],
            detail['energy_content']
        ])

    # Convert the StringIO content to bytes
    output = BytesIO()
    output.write(si.getvalue().encode('utf-8'))
    output.seek(0)

    # Send the file as a downloadable CSV
    return send_file(
        output,
        as_attachment=True,
        download_name='emission_breakdown.csv',
        mimetype='text/csv'
    )


if __name__ == '__main__':
    app.run(debug=True)