import sqlite3
from datetime import datetime, timedelta
import random

DB_PATH = "ecommerce.db"

def create_tables(cursor):
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            city TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price REAL NOT NULL,
            category TEXT NOT NULL
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            total_price REAL NOT NULL,
            order_date TEXT NOT NULL,
            status TEXT NOT NULL,
            FOREIGN KEY (customer_id) REFERENCES customers(id),
            FOREIGN KEY (product_id) REFERENCES products(id)
        )
    """)

def seed_data(cursor):
    cursor.execute("SELECT COUNT(*) FROM customers")
    if cursor.fetchone()[0] > 0:
        print("DB already seeded, skipping.")
        return

    customers = [
        ("Ahmed Khan", "ahmed@gmail.com", "Lahore"),
        ("Sara Malik", "sara@gmail.com", "Karachi"),
        ("Bilal Ahmed", "bilal@gmail.com", "Islamabad"),
        ("Fatima Zahra", "fatima@gmail.com", "Lahore"),
        ("Usman Ali", "usman@gmail.com", "Faisalabad"),
        ("Ayesha Tariq", "ayesha@gmail.com", "Karachi"),
        ("Hassan Raza", "hassan@gmail.com", "Lahore"),
        ("Zara Sheikh", "zara@gmail.com", "Islamabad"),
    ]
    for name, email, city in customers:
        cursor.execute(
            "INSERT INTO customers (name, email, city, created_at) VALUES (?, ?, ?, ?)",
            (name, email, city, datetime.now().strftime("%Y-%m-%d"))
        )

    products = [
        ("iPhone 15", 280000, "Electronics"),
        ("Samsung Galaxy S24", 220000, "Electronics"),
        ("Laptop Dell XPS", 350000, "Electronics"),
        ("Nike Air Max", 25000, "Footwear"),
        ("Levi's Jeans", 8000, "Clothing"),
        ("Sony Headphones", 45000, "Electronics"),
        ("Perfume Dior", 15000, "Beauty"),
        ("Backpack Herschel", 12000, "Accessories"),
    ]
    for name, price, category in products:
        cursor.execute(
            "INSERT INTO products (name, price, category) VALUES (?, ?, ?)",
            (name, price, category)
        )

    statuses = ["completed", "pending", "cancelled"]
    for _ in range(50):
        customer_id = random.randint(1, len(customers))
        product_id = random.randint(1, len(products))
        quantity = random.randint(1, 3)
        price = products[product_id - 1][1]
        total_price = price * quantity
        days_ago = random.randint(0, 180)
        order_date = (datetime.now() - timedelta(days=days_ago)).strftime("%Y-%m-%d")
        status = random.choice(statuses)
        cursor.execute(
            """INSERT INTO orders
               (customer_id, product_id, quantity, total_price, order_date, status)
               VALUES (?, ?, ?, ?, ?, ?)""",
            (customer_id, product_id, quantity, total_price, order_date, status)
        )

    print("DB seeded successfully.")

def setup_database():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("PRAGMA foreign_keys = ON")
        create_tables(cursor)
        seed_data(cursor)
        conn.commit()
    print(f"Database ready at {DB_PATH}")

if __name__ == "__main__":
    setup_database()
