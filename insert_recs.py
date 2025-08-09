import sqlite3
import ast

# Load user data from users.py
with open("users.py", "r") as file:
    content = file.read()

# Safely evaluate the list of dictionaries
users_data = ast.literal_eval(content.strip().split('=', 1)[1].strip())

# Connect to the people.db database
conn = sqlite3.connect("people.db")
cursor = conn.cursor()

# Create the users table if it doesn't exist
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    password TEXT,
    auth_level INTEGER
)
""")

# Insert each user record into the users table
for user in users_data:
    cursor.execute("""
    INSERT INTO users (username, password, auth_level)
    VALUES (?, ?, ?)
    """, (user["username"], str(user["password"]), user["auth_level"]))

# Commit changes and close the connection
conn.commit()
conn.close()

print("All user records have been successfully inserted into the users table.")
