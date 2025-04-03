# database.py
import sqlite3
import os

DB_PATH = "carphy.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            pin TEXT NOT NULL,
            department TEXT NOT NULL,
            role TEXT DEFAULT 'user'
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pamphlets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            department TEXT NOT NULL,
            course_name TEXT NOT NULL,
            pamphlet_name TEXT NOT NULL,
            stock INTEGER NOT NULL
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            pamphlet_name TEXT,
            quantity INTEGER,
            questions TEXT,
            instructions TEXT,
            status TEXT DEFAULT 'pending',
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)
    
    cursor.execute("SELECT COUNT(*) FROM pamphlets")
    if cursor.fetchone()[0] == 0:
        sample_pamphlets = [
            ("Business", "Marketing", "Intro to Marketing", 50),
            ("Business", "Accounting", "Basic Accounting", 30),
            ("Health Science", "Nursing", "Nursing Basics", 40),
            ("Criminal Justice", "Criminology", "Criminology 101", 20),
            ("Agriculture", "Crop Science", "Crop Basics", 25),
            ("Education", "Pedagogy", "Teaching Methods", 35)
        ]
        cursor.executemany("INSERT INTO pamphlets (department, course_name, pamphlet_name, stock) VALUES (?, ?, ?, ?)", sample_pamphlets)
    
    cursor.execute("SELECT COUNT(*) FROM users WHERE role = 'admin'")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO users (name, pin, department, role) VALUES (?, ?, ?, ?)", ("Admin", "2005mayexcellent", "Admin", "admin"))
    
    conn.commit()
    conn.close()

def add_user(name, pin, department, role="user"):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (name, pin, department, role) VALUES (?, ?, ?, ?)", (name, pin, department, role))
        user_id = cursor.lastrowid
        conn.commit()
        return user_id
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def get_user(name, pin):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT name, pin, department, role, id FROM users WHERE name = ? AND pin = ?", (name, pin))
    user = cursor.fetchone()
    conn.close()
    return user

def get_users():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, department, role FROM users")
    users = cursor.fetchall()
    conn.close()
    return users

def delete_user(user_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
    conn.commit()
    conn.close()

def get_departments():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT department FROM pamphlets")
    departments = [row[0] for row in cursor.fetchall()]
    conn.close()
    return departments

def get_courses(department):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT course_name FROM pamphlets WHERE department = ?", (department,))
    courses = [row[0] for row in cursor.fetchall()]
    conn.close()
    return courses

def get_pamphlets(department, course_name):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT pamphlet_name, stock FROM pamphlets WHERE department = ? AND course_name = ?", (department, course_name))
    pamphlets = cursor.fetchall()
    conn.close()
    return pamphlets

def add_order(user_id, pamphlet_name, quantity, questions="", instructions=""):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO orders (user_id, pamphlet_name, quantity, questions, instructions) VALUES (?, ?, ?, ?, ?)", 
                   (user_id, pamphlet_name, quantity, questions, instructions))
    cursor.execute("UPDATE pamphlets SET stock = stock - ? WHERE pamphlet_name = ?", (quantity, pamphlet_name))  # Decrease stock
    conn.commit()
    conn.close()

def get_orders(user_id=None):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    if user_id:
        cursor.execute("SELECT id, pamphlet_name, quantity, questions, instructions, status FROM orders WHERE user_id = ?", (user_id,))
    else:
        cursor.execute("SELECT id, pamphlet_name, quantity, questions, instructions, status, user_id FROM orders")
    orders = cursor.fetchall()
    conn.close()
    return orders

def update_order_status(order_id, status):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("UPDATE orders SET status = ? WHERE id = ?", (status, order_id))
    conn.commit()
    conn.close()

def update_stock(pamphlet_name, stock):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("UPDATE pamphlets SET stock = ? WHERE pamphlet_name = ?", (stock, pamphlet_name))
    conn.commit()
    conn.close()

def get_all_pamphlets():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT pamphlet_name, stock, department, course_name FROM pamphlets")
    pamphlets = cursor.fetchall()
    conn.close()
    return pamphlets  # Returns [(pamphlet_name, stock, dept, course_name), ...]

# Comment out reset after first run
# if os.path.exists(DB_PATH):
#     os.remove(DB_PATH)
init_db()