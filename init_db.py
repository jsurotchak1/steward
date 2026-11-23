import os
import sqlite3

file_path = "steward.db"

if os.path.exists(file_path):
    os.remove(file_path)

conn = sqlite3.connect(file_path)
cur = conn.cursor()

with open("schema.sql", "r", encoding="utf-8") as file:
    cur.executescript(file.read())

conn.commit()
conn.close()
print("steward.db built")