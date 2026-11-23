import sqlite3

conn = sqlite3.connect("practice.db")
cur = conn.cursor()

cur.execute("""
    CREATE TABLE IF NOT EXISTS pets (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        species TEXT
    )
""")

conn.commit()

for row in cur.execute("SELECT * FROM pets"):
    print(row[1])

conn.close()