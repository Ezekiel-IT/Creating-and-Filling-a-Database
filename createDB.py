import sqlite3

try:
    conn = sqlite3.connect('people.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            password TEXT,
            level TEXT
        )
    ''')
    
    conn.commit()
    print("Database 'people.db' and table 'users' with user_id created successfully.")
except sqlite3.Error as e:
    print(f"An error occurred: {e}")
finally:
    conn.close()
