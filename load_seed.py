import csv
import sqlite3

file_path = "steward.db"

conn = sqlite3.connect(file_path)
cur = conn.cursor()
cur.execute("PRAGMA foreign_keys = ON")

with open("seed/items.csv", mode="r", newline="", encoding="utf-8-sig") as file:
    reader = csv.DictReader(file)
    for row in reader:
        cur.execute("INSERT OR IGNORE INTO items (name, category, meal, unit, store) VALUES (?, ?, ?, ?, ?)",
                    (row["name"].strip(), row["category"].strip(), row["meal"].strip(), row["unit"].strip(), row["store"].strip()))

conn.commit()
cur.execute("SELECT COUNT(*) FROM items")
(count,) = cur.fetchone()
print(f"Items in table: {count}")
conn.close()