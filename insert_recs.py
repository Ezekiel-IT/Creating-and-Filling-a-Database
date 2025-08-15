import sqlite3
from users import users_data  # Make sure this matches your actual filename

conn = sqlite3.connect('people.db')
cursor = conn.cursor()

for user in users_data:
    cursor.execute(
        "INSERT INTO users (username, password, level) VALUES (:username, :password, :auth_level)",
        user
    )

conn.commit()
conn.close()
print("User records inserted successfully.")
