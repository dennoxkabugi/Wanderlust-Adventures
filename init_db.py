# init_db.py
import sqlite3

def initialize_db():
    conn = sqlite3.connect('tourists.db')
    cursor = conn.cursor()

    # Create the Tourist table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Tourist (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL
    )
    ''')

    # Create the Trip table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Trip (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tourist_id INTEGER,
        destination TEXT NOT NULL,
        arrival_date TEXT NOT NULL,
        departure_date TEXT NOT NULL,
        days INTEGER NOT NULL,
        accommodation TEXT NOT NULL,
        total INTEGER NOT NULL,
        FOREIGN KEY (tourist_id) REFERENCES Tourist(id)
    )
    ''')

    conn.commit()
    conn.close()

if __name__ == '__main__':
    initialize_db()
    print('Database initialized.')
