import sqlite3

# Connect to the SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('Z:/Magontec testing/emission_factors.db')
cursor = conn.cursor()

# Drop the existing EmissionFactors table if you want to reset it
cursor.execute('''
DROP TABLE IF EXISTS EmissionFactors
''')

# Create the EmissionFactors table
cursor.execute('''
CREATE TABLE IF NOT EXISTS EmissionFactors (
    id INTEGER PRIMARY KEY,
    emission_type TEXT,
    energy_content REAL,
    emission_factor REAL
)
''')

# Insert the full list of data
data = [
    ("Electricity", 1, 0.65),
    ("Bituminous coal", 27, 90.24),
    ("Sub-bituminous coal", 21, 90.24),
    ("Anthracite", 29, 90.24),
    ("Brown coal (lignite)", 10.2, 93.82),
    ("Coking coal", 30, 92.03),
    ("Coal briquettes", 22.1, 95.38),
    ("Coal coke", 27, 107.23),
    ("Coal tar", 37.5, 82.03),
    ("Solid fossil fuels other than those mentioned in the items above", 22.1, 95.28),
    ("Industrial materials derived from fossil fuels, if recycled and combusted", 26.3, 81.83),
    ("Passenger car tyres, if recycled and combusted", 32, 63.03),
    ("Truck and off-road tyres, if recycled and combusted", 27.1, 56.13),
    ("Non-biomass municipal materials, if combusted", 10.5, 88.9),
    ("Dry wood", 16.2, 1.2),
    ("Green and air dried wood", 10.4, 1.2),
    ("Sulphite lyes", 12.4, 0.58),
    ("Bagasse", 9.6, 1.4),
    ("Biomass, municipal and industrial materials, if combusted", 12.2, 1.8),
    ("Charcoal", 31.1, 6.3),
    ("Primary solid biomass fuels other than those mentioned above", 12.2, 1.8),
    ("Natural gas distributed in a pipeline", 0.0393, 51.53),
    ("Coal seam methane captured for combustion", 0.0377, 51.63),
    ("Coal mine waste gas captured for combustion", 0.0377, 56.8),
    ("Compressed natural gas (reverting to standard conditions)", 0.0393, 51.53),
    ("Unprocessed natural gas", 0.0393, 51.53),
    ("Ethane", 0.0629, 56.56),
    ("Coke oven gas", 0.0181, 37.08),
    ("Blast furnace gas", 0.004, 234.05),
    ("Town gas", 0.039, 60.27),
    ("Liquefied natural gas", 25.3, 51.53),
    ("Gaseous fossil fuels other than those mentioned above", 0.039, 51.53),
    ("Landfill biogas captured for combustion (methane only)", 0.0377, 6.43),
    ("Sludge biogas captured for combustion (methane only)", 0.0377, 6.43),
    ("Biogas captured for combustion, other than those mentioned above", 0.037, 6.43),
    ("Biomethane", 0.0393, 0.13),
    ("Petroleum-based oils (non-fuel)", 38.8, 13.9),
    ("Petroleum-based greases", 38.8, 3.5),
    ("Crude oil including crude oil condensates", 45.3, 69.88),
    ("Other natural gas liquids", 46.5, 61.28),
    ("Automotive gasoline/petrol (non-aircraft fuel)", 34.2, 67.8),
    ("Aviation gasoline", 33.1, 67.4),
    ("Kerosene (non-aircraft fuel)", 37.5, 69.11),
    ("Aviation turbine fuel/kerosene", 36.8, 69.82),
    ("Heating oil", 37.3, 69.73),
    ("Diesel oil", 38.6, 70.2),
    ("Fuel oil", 39.7, 73.84),
    ("Liquefied aromatic hydrocarbons", 34.4, 69.93),
    ("Solvents: mineral turpentine or white spirits", 34.4, 69.93),
    ("Liquefied petroleum gas (LPG)", 25.7, 60.6),
    ("Naphtha", 31.4, 69.82),
    ("Petroleum coke", 29.5, 92.88),
    ("Refinery gas and liquids", 42.9, 54.76),
    ("Refinery coke", 42.9, 92.88),
    ("Other petroleum-based products", 34.4, 69.92),
    ("Biodiesel", 34.6, 0.28),
    ("Ethanol for use as a fuel in an internal combustion engine", 23.4, 0.28),
    ("Biofuels other than those mentioned above and below", 23.4, 0.28),
    ("Renewable aviation kerosene", 36.8, 0.22),
    ("Renewable diesel", 38.6, 0.3),
    ("Gasoline", 34.2, 67.62),
    ("Diesel oil", 38.6, 70.41),
    ("Liquefied petroleum gas (LPG)", 25.7, 61),
    ("Fuel oil", 39.7, 74.18),
    ("Ethanol", 23.7, 0.4),
    ("Biodiesel", 34.6, 2.5),
    ("Renewable diesel", 38.6, 0.51),
    ("Other biofuels", 23.4, 2.5),
    ("Compressed natural gas", 0.0393, 59),
    ("Liquefied natural gas", 25.3, 59),
    ("Compressed natural gas", 0.0393, 54.5),
    ("Liquefied natural gas", 25.3, 54.5),
    ("Diesel oil - Euro iv or higher", 38.6, 70.37),
    ("Diesel oil - Euro iii", 38.6, 70.4),
    ("Diesel oil - Euro i", 38.6, 70.5),
    ("Renewable diesel – Euro iv or higher", 38.6, 0.47),
    ("Renewable diesel – Euro iii", 38.6, 0.5),
    ("Renewable diesel – Euro i", 38.6, 0.6),
    ("Gasoline for use as fuel in an aircraft", 33.1, 67.66),
    ("Kerosene for use as fuel in an aircraft", 36.8, 70.21),
    ("Renewable aviation kerosene", 36.8, 0.61),
    ("Limestone (calcium carbonate)", None, 0.44),
    ("Magnesium carbonate", None, 0.522),
    ("Dolomite", None, 0.477),
    ("Soda Ash Use", None, 0.415),
    ("Unmanaged aerobic treatment", None, 0.1229),
    ("Anaerobic digester/reactor", None, 0.3276),
    ("Anaerobic lagoon shallow (<2 metres)", None, 0.0819),
    ("Anaerobic lagoon deep (>2 metres)", None, 0.3276),
    ("Clinical Waste", None, 0.879),
    ("Fossil Liquid", None, 2.931),
    ("Industrial Waste", None, 1.649),
    ("Municipal Solid Waste", None, 0.0537),
    ("Composting", None, 0.046),
    ("Anaerobic digestion", None, 0.028)
]

# Insert data into the table
cursor.executemany('''
    INSERT INTO EmissionFactors (emission_type, energy_content, emission_factor)
    VALUES (?, ?, ?)
''', data)

# Commit and close the connection
conn.commit()
conn.close()

print("Energy emission factors inserted successfully!")

