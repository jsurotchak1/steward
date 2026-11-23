import csv
import sqlite3

file_path = "steward.db"

conn = sqlite3.connect(file_path)
cur = conn.cursor()
cur.execute("PRAGMA foreign_keys = ON")

with open("seed/meal_ingredients.csv", mode="r", newline="", encoding="utf-8-sig") as file:
    rows = list(csv.DictReader(file))

# Stage A: make sure every meal in the CSV exists in the meals table
meal_names = {row["meal"].strip() for row in rows}
for name in meal_names:
    cur.execute("INSERT OR IGNORE INTO meals (name) VALUES (?)", (name,))

# Stage B: translate names to ids, then insert
skipped = 0
for row in rows:
    meal_name = row["meal"].strip()
    item_name = row["item"].strip()

    cur.execute("SELECT id FROM meals WHERE name = ?", (meal_name,))
    meal_result = cur.fetchone()
    if meal_result is None:
        print(f"Warning: meal not found: {meal_name}")
        skipped += 1
        continue
    (meal_id,) = meal_result

    cur.execute("SELECT id FROM items WHERE name = ?", (item_name,))
    item_result = cur.fetchone()
    if item_result is None:
        print(f"Warning: item not found: {item_name} (meal: {meal_name})")
        skipped += 1
        continue
    (item_id,) = item_result

    cur.execute(
        "INSERT OR IGNORE INTO meal_ingredients (meal_id, item_id, usual_qty) VALUES (?, ?, ?)",
        (meal_id, item_id, float(row["quantity"].strip())),
    )

conn.commit()

cur.execute("SELECT COUNT(*) FROM meals")
(meal_count,) = cur.fetchone()
cur.execute("SELECT COUNT(*) FROM meal_ingredients")
(ingredient_count,) = cur.fetchone()

print(f"Meals: {meal_count}, ingredient rows: {ingredient_count}, skipped: {skipped}")
conn.close()