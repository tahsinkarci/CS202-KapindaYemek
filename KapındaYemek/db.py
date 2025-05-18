import mysql.connector
from datetime import datetime

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="#123321#%&",
        database="project"
    )

def get_user_by_username(username):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT user_id, password FROM User WHERE username=%s", (username,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result

def username_exists(username):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM User WHERE username=%s", (username,))
    exists = cursor.fetchone() is not None
    cursor.close()
    conn.close()
    return exists

def is_manager(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Manager WHERE user_id=%s", (user_id,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result is not None

def is_customer(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Customer WHERE user_id=%s", (user_id,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result is not None

def get_last_user_id():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT user_id FROM User ORDER BY user_id DESC LIMIT 1")
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result[0] if result else None

def get_last_customer_id():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT customer_id FROM Customer ORDER BY customer_id DESC LIMIT 1")
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result[0] if result else None

def insert_user(user_id, username, password, first_name, last_name):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO User (user_id, username, password, first_name, last_name) VALUES (%s, %s, %s, %s, %s)",
        (user_id, username, password, first_name, last_name)
    )
    conn.commit()
    cursor.close()
    conn.close()

def insert_customer(customer_id, user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO Customer (customer_id, user_id, signup_date) VALUES (%s, %s, %s)",
        (customer_id, user_id, datetime.now())
    )
    conn.commit()
    cursor.close()
    conn.close()

def get_all_customers():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Customer")
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return data

def listAllMenuItemsByIDOfRestaurant(self, restaurant_id): # workbenchte calısıo
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT m.name,m.price"
                    "FROM restaurant r"
                    "JOIN offers o ON r.restaurant_id = o.restaurant_id"
                    "JOIN menuitem m ON o.menu_item_id  = m.menu_item_id"
                    "WHERE r.restaurant_id = %s", (restaurant_id))
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return data

def createCart(self, cart_id, status, total_amount):  # in menu page the total am. needs to be calculated
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Cart (cart_id, status, created_at, updated_at, total_amount)"
                   " VALUES (%s, %s, %s,%s, %s)",
        (cart_id, status, datetime.now(), datetime.now(), total_amount))
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return data

def deleteCart(self, cart_id):
    conn   = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM Cart WHERE cart_id = %s",
        (cart_id,)
    )
    deleted = cursor.rowcount
    cursor.close()
    conn.close()
    return deleted
