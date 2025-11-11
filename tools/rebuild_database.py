#!/usr/bin/env python3
"""
MEDUSA CTF - Database Rebuild Script
Creates medusa.db with 12 dummy tables and 100+ rows of dummy data
"""

import sqlite3
import os
import random
from datetime import datetime, timedelta

DB_PATH = "../assets/medusa.db"

# Sample data for generating dummy entries
FIRST_NAMES = ["John", "Jane", "Alice", "Bob", "Charlie", "Diana", "Edward", "Fiona", "George", "Hannah",
               "Ivan", "Julia", "Kevin", "Laura", "Michael", "Nancy", "Oscar", "Patricia", "Quinn", "Rachel",
               "Samuel", "Teresa", "Ulysses", "Victoria", "Walter", "Xena", "Yolanda", "Zachary"]

LAST_NAMES = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez",
              "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson", "Thomas", "Taylor", "Moore", "Jackson", "Martin",
              "Lee", "Perez", "Thompson", "White", "Harris", "Sanchez", "Clark", "Ramirez", "Lewis", "Robinson"]

CITIES = ["New York", "Los Angeles", "Chicago", "Houston", "Phoenix", "Philadelphia", "San Antonio", "San Diego",
          "Dallas", "San Jose", "Austin", "Jacksonville", "Fort Worth", "Columbus", "Charlotte", "San Francisco",
          "Indianapolis", "Seattle", "Denver", "Washington", "Boston", "Nashville", "Detroit", "Portland"]

DEPARTMENTS = ["Engineering", "Marketing", "Sales", "HR", "Finance", "IT", "Operations", "Customer Support",
               "Research", "Development", "Design", "Security", "Legal", "Logistics"]

PRODUCTS = ["Widget A", "Gadget B", "Device C", "Tool D", "Component E", "Module F", "System G", "Platform H",
            "Service I", "Solution J", "Package K", "Bundle L", "Kit M", "Set N", "Unit O"]

COMPANIES = ["TechCorp", "DataSys", "CloudNet", "SecureIT", "FastCode", "SmartSoft", "MegaByte", "CyberLink",
             "NetWave", "InfoTech", "DigiCore", "ByteFlow", "CodeCraft", "SoftWorks", "TechFlow"]


def generate_email(first_name, last_name, suffix=""):
    """Generate an email address"""
    domains = ["example.com", "techcorp.com", "email.com", "business.net", "company.org"]
    return f"{first_name.lower()}.{last_name.lower()}{suffix}@{random.choice(domains)}"


def generate_phone():
    """Generate a random phone number"""
    return f"+1-{random.randint(200, 999)}-{random.randint(100, 999)}-{random.randint(1000, 9999)}"


def random_date(start_year=2020, end_year=2025):
    """Generate a random date"""
    start = datetime(start_year, 1, 1)
    end = datetime(end_year, 12, 31)
    delta = end - start
    random_days = random.randint(0, delta.days)
    return (start + timedelta(days=random_days)).strftime("%Y-%m-%d")


def rebuild_database():
    """Rebuild the entire database with dummy data"""
    
    # Get the script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(script_dir, DB_PATH)
    
    # Remove existing database
    if os.path.exists(db_path):
        os.remove(db_path)
        print(f"🗑️  Removed existing database")
    
    # Ensure assets directory exists
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    
    # Create new database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    print("🔨 Creating database with 12 tables...")
    
    # Table 1: credentials (the actual table used by the app)
    print("  📋 Creating table 1/12: credentials")
    cursor.execute("""
        CREATE TABLE credentials (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)

    # Add the actual credentials
    cursor.execute("INSERT INTO credentials (username, password) VALUES (?, ?)", 
                   ("perseus", "m3dus4_sl4y3r"))
    
    # Add Greek god credentials
    cursor.execute("INSERT INTO credentials (username, password) VALUES (?, ?)",
               ("hercules", "n3m34n_l10n"))
    cursor.execute("INSERT INTO credentials (username, password) VALUES (?, ?)",
                ("athena", "0w1_of_w1sd0m"))
    cursor.execute("INSERT INTO credentials (username, password) VALUES (?, ?)",
                ("zeus", "thund3r_b0lt"))
    cursor.execute("INSERT INTO credentials (username, password) VALUES (?, ?)",
                ("poseidon", "tr1d3nt_k1ng"))
    cursor.execute("INSERT INTO credentials (username, password) VALUES (?, ?)",
                ("aphrodite", "b34uty_qu33n"))
    cursor.execute("INSERT INTO credentials (username, password) VALUES (?, ?)",
                ("ares", "w4r_g0d"))
    cursor.execute("INSERT INTO credentials (username, password) VALUES (?, ?)",
                ("artemis", "hunt3r_m00n"))
    cursor.execute("INSERT INTO credentials (username, password) VALUES (?, ?)",
                ("apollo", "s0lar_fl4r3"))
    cursor.execute("INSERT INTO credentials (username, password) VALUES (?, ?)",
                ("hephaestus", "f0rg3_m4st3r"))
    cursor.execute("INSERT INTO credentials (username, password) VALUES (?, ?)",
                ("dionysus", "w1n3_g0d"))
    cursor.execute("INSERT INTO credentials (username, password) VALUES (?, ?)",
                ("hermes", "m3ss3ng3r"))
    cursor.execute("INSERT INTO credentials (username, password) VALUES (?, ?)",
                ("hades", "und3rw0rld_k1ng"))
    cursor.execute("INSERT INTO credentials (username, password) VALUES (?, ?)",
                ("demeter", "h4rv3st_g0dd3ss"))

    # Add 120 dummy credentials
    for i in range(120):
        username = f"user{i+1:03d}"
        password = f"pass{random.randint(1000, 9999)}"
        cursor.execute("INSERT INTO credentials (username, password) VALUES (?, ?)", 
                       (username, password))
    
    # Table 2: employees
    print("  📋 Creating table 2/12: employees")
    cursor.execute("""
        CREATE TABLE employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            phone TEXT,
            department TEXT,
            hire_date TEXT,
            salary REAL
        )
    """)
    
    for i in range(150):
        first_name = random.choice(FIRST_NAMES)
        last_name = random.choice(LAST_NAMES)
        cursor.execute("""
            INSERT INTO employees (first_name, last_name, email, phone, department, hire_date, salary)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            first_name,
            last_name,
            generate_email(first_name, last_name, f"{i+1}"),
            generate_phone(),
            random.choice(DEPARTMENTS),
            random_date(2018, 2024),
            round(random.uniform(40000, 150000), 2)
        ))
    
    # Table 3: customers
    print("  📋 Creating table 3/12: customers")
    cursor.execute("""
        CREATE TABLE customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company_name TEXT NOT NULL,
            contact_name TEXT,
            email TEXT,
            phone TEXT,
            city TEXT,
            country TEXT,
            registration_date TEXT
        )
    """)
    
    for i in range(180):
        cursor.execute("""
            INSERT INTO customers (company_name, contact_name, email, phone, city, country, registration_date)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            random.choice(COMPANIES) + f" {i+1}",
            f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}",
            generate_email(random.choice(FIRST_NAMES), random.choice(LAST_NAMES), f"{i+1000}"),
            generate_phone(),
            random.choice(CITIES),
            "USA",
            random_date(2019, 2025)
        ))
    
    # Table 4: products
    print("  📋 Creating table 4/12: products")
    cursor.execute("""
        CREATE TABLE products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_name TEXT NOT NULL,
            category TEXT,
            price REAL,
            stock_quantity INTEGER,
            supplier_id INTEGER,
            created_date TEXT
        )
    """)
    
    categories = ["Electronics", "Software", "Hardware", "Services", "Consulting"]
    for i in range(200):
        cursor.execute("""
            INSERT INTO products (product_name, category, price, stock_quantity, supplier_id, created_date)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            random.choice(PRODUCTS) + f" {i+1}",
            random.choice(categories),
            round(random.uniform(9.99, 999.99), 2),
            random.randint(0, 1000),
            random.randint(1, 50),
            random_date(2020, 2025)
        ))
    
    # Table 5: orders
    print("  📋 Creating table 5/12: orders")
    cursor.execute("""
        CREATE TABLE orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER,
            order_date TEXT,
            total_amount REAL,
            status TEXT,
            shipping_address TEXT
        )
    """)
    
    statuses = ["Pending", "Processing", "Shipped", "Delivered", "Cancelled"]
    for i in range(250):
        cursor.execute("""
            INSERT INTO orders (customer_id, order_date, total_amount, status, shipping_address)
            VALUES (?, ?, ?, ?, ?)
        """, (
            random.randint(1, 180),
            random_date(2022, 2025),
            round(random.uniform(50, 5000), 2),
            random.choice(statuses),
            f"{random.randint(100, 9999)} {random.choice(['Main St', 'Oak Ave', 'Maple Dr', 'Pine Rd'])}"
        ))
    
    # Table 6: transactions
    print("  📋 Creating table 6/12: transactions")
    cursor.execute("""
        CREATE TABLE transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER,
            transaction_date TEXT,
            amount REAL,
            payment_method TEXT,
            transaction_id TEXT
        )
    """)
    
    payment_methods = ["Credit Card", "Debit Card", "PayPal", "Bank Transfer", "Cash"]
    for i in range(300):
        cursor.execute("""
            INSERT INTO transactions (order_id, transaction_date, amount, payment_method, transaction_id)
            VALUES (?, ?, ?, ?, ?)
        """, (
            random.randint(1, 250),
            random_date(2022, 2025),
            round(random.uniform(50, 5000), 2),
            random.choice(payment_methods),
            f"TXN{random.randint(100000, 999999)}"
        ))
    
    # Table 7: inventory
    print("  📋 Creating table 7/12: inventory")
    cursor.execute("""
        CREATE TABLE inventory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER,
            warehouse_location TEXT,
            quantity INTEGER,
            last_updated TEXT
        )
    """)
    
    warehouses = ["Warehouse A", "Warehouse B", "Warehouse C", "Distribution Center 1", "Distribution Center 2"]
    for i in range(150):
        cursor.execute("""
            INSERT INTO inventory (product_id, warehouse_location, quantity, last_updated)
            VALUES (?, ?, ?, ?)
        """, (
            random.randint(1, 200),
            random.choice(warehouses),
            random.randint(0, 500),
            random_date(2024, 2025)
        ))
    
    # Table 8: reviews
    print("  📋 Creating table 8/12: reviews")
    cursor.execute("""
        CREATE TABLE reviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER,
            customer_id INTEGER,
            rating INTEGER,
            review_text TEXT,
            review_date TEXT
        )
    """)
    
    review_texts = [
        "Great product, highly recommend!",
        "Good value for money.",
        "Not what I expected.",
        "Excellent quality and fast shipping.",
        "Average product, nothing special.",
        "Disappointed with the quality.",
        "Best purchase I've made!",
        "Works as described."
    ]
    
    for i in range(220):
        cursor.execute("""
            INSERT INTO reviews (product_id, customer_id, rating, review_text, review_date)
            VALUES (?, ?, ?, ?, ?)
        """, (
            random.randint(1, 200),
            random.randint(1, 180),
            random.randint(1, 5),
            random.choice(review_texts),
            random_date(2022, 2025)
        ))
    
    # Table 9: suppliers
    print("  📋 Creating table 9/12: suppliers")
    cursor.execute("""
        CREATE TABLE suppliers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company_name TEXT NOT NULL,
            contact_person TEXT,
            email TEXT,
            phone TEXT,
            address TEXT,
            country TEXT
        )
    """)
    
    for i in range(50):
        cursor.execute("""
            INSERT INTO suppliers (company_name, contact_person, email, phone, address, country)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            random.choice(COMPANIES) + f" Supplies {i+1}",
            f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}",
            generate_email(random.choice(FIRST_NAMES), random.choice(LAST_NAMES), f"sup{i+1}"),
            generate_phone(),
            f"{random.randint(100, 9999)} {random.choice(['Business Blvd', 'Commerce St', 'Industrial Ave'])}",
            random.choice(["USA", "Canada", "Mexico", "UK", "Germany"])
        ))
    
    # Table 10: system_logs
    print("  📋 Creating table 10/12: system_logs")
    cursor.execute("""
        CREATE TABLE system_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            log_level TEXT,
            message TEXT,
            user_id INTEGER,
            ip_address TEXT,
            timestamp TEXT
        )
    """)
    
    log_levels = ["INFO", "WARNING", "ERROR", "DEBUG", "CRITICAL"]
    log_messages = [
        "User login successful",
        "Failed login attempt",
        "Database connection established",
        "API request processed",
        "Cache cleared",
        "Configuration updated",
        "Backup completed",
        "Session timeout"
    ]
    
    for i in range(350):
        cursor.execute("""
            INSERT INTO system_logs (log_level, message, user_id, ip_address, timestamp)
            VALUES (?, ?, ?, ?, ?)
        """, (
            random.choice(log_levels),
            random.choice(log_messages),
            random.randint(1, 150),
            f"{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}",
            random_date(2024, 2025) + f" {random.randint(0, 23):02d}:{random.randint(0, 59):02d}:{random.randint(0, 59):02d}"
        ))
    
    # Table 11: sessions
    print("  📋 Creating table 11/12: sessions")
    cursor.execute("""
        CREATE TABLE sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            session_token TEXT,
            ip_address TEXT,
            user_agent TEXT,
            created_at TEXT,
            expires_at TEXT
        )
    """)
    
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
        "Mozilla/5.0 (X11; Linux x86_64)",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X)"
    ]
    
    for i in range(180):
        cursor.execute("""
            INSERT INTO sessions (user_id, session_token, ip_address, user_agent, created_at, expires_at)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            random.randint(1, 150),
            f"sess_{random.randint(100000000, 999999999)}_{random.randint(1000, 9999)}",
            f"{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}",
            random.choice(user_agents),
            random_date(2024, 2025),
            random_date(2025, 2025)
        ))
    
    # Table 12: api_keys
    print("  📋 Creating table 12/12: api_keys")
    cursor.execute("""
        CREATE TABLE api_keys (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            key_name TEXT,
            api_key TEXT UNIQUE,
            user_id INTEGER,
            permissions TEXT,
            created_date TEXT,
            last_used TEXT,
            is_active INTEGER
        )
    """)
    
    permissions_list = ["read", "write", "admin", "read,write", "read,write,admin"]
    
    for i in range(100):
        cursor.execute("""
            INSERT INTO api_keys (key_name, api_key, user_id, permissions, created_date, last_used, is_active)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            f"API Key {i+1}",
            f"sk_{random.randint(10000000, 99999999)}_{random.randint(10000000, 99999999)}",
            random.randint(1, 150),
            random.choice(permissions_list),
            random_date(2023, 2025),
            random_date(2024, 2025),
            random.randint(0, 1)
        ))
    
    # Commit and close
    conn.commit()
    conn.close()
    
    print("\n✅ Database rebuilt successfully!")
    print(f"📁 Location: {db_path}")
    print("\n📊 Summary:")
    print(f"   - credentials: 121 rows (1 valid + 120 dummy)")
    print(f"   - employees: 150 rows")
    print(f"   - customers: 180 rows")
    print(f"   - products: 200 rows")
    print(f"   - orders: 250 rows")
    print(f"   - transactions: 300 rows")
    print(f"   - inventory: 150 rows")
    print(f"   - reviews: 220 rows")
    print(f"   - suppliers: 50 rows")
    print(f"   - system_logs: 350 rows")
    print(f"   - sessions: 180 rows")
    print(f"   - api_keys: 100 rows")
    print(f"\n   TOTAL: 2,251 rows across 12 tables")
    print("\n🔑 Valid credentials: perseus / m3dus4_sl4y3r")


if __name__ == "__main__":
    rebuild_database()

