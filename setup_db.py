import sqlite3

conn = sqlite3.connect('emission_factors.db')
cursor = conn.cursor()

# Drop the EmissionFactors table if it already exists to avoid duplicates
cursor.execute('DROP TABLE IF EXISTS EmissionFactors')

# Create the EmissionFactors table if it doesn't exist
cursor.execute('''
CREATE TABLE IF NOT EXISTS EmissionFactors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    emission_type TEXT,
    unit TEXT,
    emission_factor REAL,
    energy_content REAL
)
''')

# Insert the full list of data
data = [
    ("Electricity", "kWh", 0.65, 1),
    ("Electricity", "MWh", 650, 1),
    ("Bituminous coal", "Kg", 90.24, 27),
    ("Bituminous coal", "Tonnes", 90.24, 27000),
    ("Sub-bituminous coal", "Kg", 90.24, 21),
    ("Sub-bituminous coal", "Tonnes", 90.24, 21000),
    ("Anthracite", "Kg", 90.24, 29),
    ("Anthracite", "Tonnes", 90.24, 29000),
    ("Brown coal (lignite)", "Kg", 93.82, 10.2),
    ("Brown coal (lignite)", "Tonnes", 93.82, 10200),
    ("Coking coal", "Kg", 92.03, 30),
    ("Coking coal", "Tonnes", 92.03, 30000),
    ("Coal briquettes", "Kg", 95.38, 22.1),
    ("Coal briquettes", "Tonnes", 95.38, 22100),
    ("Coal coke", "Kg", 107.23, 27),
    ("Coal coke", "Tonnes", 107.23, 27000),
    ("Coal tar", "Kg", 82.03, 37.5),
    ("Coal tar", "Tonnes", 82.03, 37500),
    ("Natural gas", "Cubic meters", 51.53, 0.0393),
    ("Natural gas", "Cubic feet", 51.53, 1.39),
    ("Liquefied natural gas", "Liters", 51.53, 25.3),
    ("Liquefied natural gas", "Gallons", 51.53, 95.7),
    ("Gasoline", "Liters", 67.62, 34.2),
    ("Gasoline", "Gallons", 67.62, 129.72),
    ("Diesel oil", "Liters", 70.41, 38.6),
    ("Diesel oil", "Gallons", 70.41, 146.13),
    ("Biodiesel", "Liters", 0.28, 34.6),
    ("Biodiesel", "Gallons", 0.28, 131.1),
    ("Bagasse", "Kg", 1.4, 9.6),
    ("Charcoal", "Kg", 6.3, 31.1),
    ("Petroleum-based oils", "Liters", 13.9, 38.8),
    ("Petroleum-based oils", "Gallons", 13.9, 146.9),
    ("Crude oil", "Liters", 69.88, 45.3),
    ("Crude oil", "Gallons", 69.88, 171.48),
    ("Kerosene", "Liters", 69.11, 37.5),
    ("Kerosene", "Gallons", 69.11, 141.75),
    ("Fuel oil", "Liters", 73.84, 39.7),
    ("Fuel oil", "Gallons", 73.84, 149.85),
    ("Naphtha", "Liters", 69.82, 31.4),
    ("Naphtha", "Gallons", 69.82, 118.9),
    ("Liquefied petroleum gas (LPG)", "Liters", 60.6, 25.7),
    ("Liquefied petroleum gas (LPG)", "Gallons", 60.6, 97.29),
    ("Ethanol", "Liters", 0.4, 23.7),
    ("Ethanol", "Gallons", 0.4, 89.73),
    ("Compressed natural gas", "Cubic meters", 54.5, 0.0393),
    ("Compressed natural gas", "Cubic feet", 54.5, 1.93),
    ("Renewable diesel", "Liters", 0.51, 38.6),
    ("Renewable diesel", "Gallons", 0.51, 146.13),
    ("Limestone", "Kg", 0.44, None),
    ("Dolomite", "Kg", 0.477, None),
    ("Soda Ash Use", "Kg", 0.415, None),
    ("Clinical Waste", "Kg", 0.879, None),
    ("Industrial Waste", "Kg", 1.649, None),
    ("Municipal Solid Waste", "Kg", 0.0537, None),
    ("Composting", "Kg", 0.046, None),
    ("Anaerobic digestion", "Kg", 0.028, None),
    ("Solid fossil fuels", "Kg", 95.28, 22.1),
    ("Industrial fossil materials", "Kg", 81.83, 26.3),
    ("Passenger car tyres", "Kg", 63.03, 32),
    ("Truck tyres", "Kg", 56.13, 27.1),
    ("Non-biomass municipal materials", "Kg", 88.9, 10.5),
    ("Dry wood", "Kg", 1.2, 16.2),
    ("Green and air dried wood", "Kg", 1.2, 10.4),
    ("Sulphite lyes", "Kg", 0.58, 12.4),
    ("Biomass and industrial materials", "Kg", 1.8, 12.2),
]

# Insert data into the table
cursor.executemany('''
    INSERT INTO EmissionFactors (emission_type, unit, energy_content, emission_factor)
    VALUES (?, ?, ?, ?)
''', data)

# Commit and close the connection
conn.commit()
conn.close()

print("Energy emission factors inserted successfully!")

