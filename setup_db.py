import sqlite3

# Source database
source = sqlite3.connect("finance_legacy_orders.db")
sc = source.cursor()
sc.execute("""
CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY,
    customer_name TEXT NOT NULL,
    amount INTEGER NOT NULL
)
""")
sc.executemany(
    "INSERT OR REPLACE INTO orders VALUES (?, ?, ?)",
    [
        (1, "Rahul Sharma", 1200),
        (2, "Anita Verma", 900),
        (3, "Sanjay Patel", -500),
        (4, "Neha Kapoor", 1600)
    ]
)
source.commit()
source.close()

# Target database
target = sqlite3.connect("finance_modern_orders.db")
tc = target.cursor()
tc.execute("""
CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY,
    customer_name TEXT NOT NULL,
    amount INTEGER NOT NULL
)
""")
target.commit()
target.close()

print("Databases initialized successfully")
