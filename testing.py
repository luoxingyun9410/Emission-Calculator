import sqlite3

conn = sqlite3.connect('Z:/Magontec testing/emission_factors.db')
cursor = conn.cursor()

# Delete all duplicate entries for "Electricity"
cursor.execute('''
DELETE FROM EmissionFactors WHERE emission_type = 'Electricity'
''')

conn.commit()

# Insert the correct single entry for "Electricity"
cursor.execute('''
INSERT INTO EmissionFactors (emission_type, energy_content, emission_factor)
VALUES (?, ?, ?)
''', ("Electricity", 1.0, 0.65))

conn.commit()
conn.close()

print("Duplicates removed and single entry for 'Electricity' added.")


