from flask import Flask, request, render_template
import sqlite3
import spacy

# Load the NLP model
nlp = spacy.load('en_core_web_md')

def find_best_match(user_input):
    # Connect to the SQLite database
    conn = sqlite3.connect("Z:/Magontec testing/emission_factors.db")
    cursor = conn.cursor()

    # Fetch all emission types and factors from the database
    cursor.execute("SELECT emission_type, energy_content, emission_factor FROM EmissionFactors")
    rows = cursor.fetchall()
    conn.close()

    best_match = None
    best_score = float('-inf')

    # Find the closest match for the user's input
    user_doc = nlp(user_input)
    for row in rows:
        emission_doc = nlp(row[0])
        similarity = user_doc.similarity(emission_doc)
        if similarity > best_score:
            best_match = row
            best_score = similarity

    # Return matched emission type, energy content, and emission factor
    return best_match

app = Flask(__name__)

# Route for the homepage
@app.route('/')
def index():
    return render_template('index.html')

# Route for calculations
@app.route('/calculate', methods=['POST'])
def calculate():
    emission_type = request.form['emission_type']
    volume = float(request.form['volume']) / 1000  # Convert liters to kL

    # Fetch emission factors from the database
    matched_emission_type, energy_content, emission_factor = find_best_match(emission_type)

    # Calculate emissions based on whether energy_content is provided
    if energy_content is None or energy_content == 0:
        # If energy content is None or 0, use only the emission factor and volume
        emissions_kg = volume * emission_factor
    else:
        # Otherwise, include energy content in the calculation
        emissions_kg = volume * energy_content * emission_factor

    # Convert emissions from kg CO2-e to t CO2-e
    emissions_t = emissions_kg / 1000

    # Format emissions to scientific notation
    emissions_t_scientific = "{:.2e}".format(emissions_t)

    # Pass all variables to the results page for display
    return render_template('results.html',
                           emissions=emissions_t_scientific,
                           emission_type=matched_emission_type,
                           volume=volume,
                           energy_content=energy_content,
                           emission_factor=emission_factor)

if __name__ == '__main__':
    app.run(debug=True)

