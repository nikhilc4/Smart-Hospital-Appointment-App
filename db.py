def create_tables():
    import sqlite3
    conn = sqlite3.connect("hospital.db")
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS patients (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT,
                        age INTEGER,
                        issue TEXT,
                        doctor TEXT,
                        date TEXT,
                        time TEXT,
                        email TEXT,
                        status TEXT DEFAULT 'waiting'
                    )''')
    conn.commit()
    conn.close()
