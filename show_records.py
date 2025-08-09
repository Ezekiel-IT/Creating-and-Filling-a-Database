import sqlite3

# Connect to the people.db database
conn = sqlite3.connect('people.db')
cursor = conn.cursor()

# Query to select all records from the users table
cursor.execute("SELECT * FROM users")
records = cursor.fetchall()

# Print each record
for record in records:
    print(record)

# Close the connection
conn.close()