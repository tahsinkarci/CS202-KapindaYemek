import mysql.connector
from datetime import datetime

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="tHfB1848*D2#",
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

