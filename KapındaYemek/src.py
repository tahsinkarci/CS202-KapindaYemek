from flask import Flask, render_template
from flask import request, redirect, url_for, flash
import mysql.connector
from datetime import datetime
print("Connector is working!")


app = Flask(__name__)
app.secret_key = "asdasfamanasqwezayras"  # Add this line

@app.route("/")
def home():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="your_unique_db_pass",  # enter YOUR db password
        database="project"
    )
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Customer")
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template("index.html", data=data)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="your_unique_db_pass",
            database="project"
        )
        cursor = conn.cursor()
        # first, check if the username exists
        cursor.execute("SELECT user_id, password FROM User WHERE username=%s", (username,))
        result = cursor.fetchone()

        if not result:
            flash("Username not found. Please register first.")
            cursor.close()
            conn.close()
            return render_template("login.html")
        
        user_id, db_password = result # if there is a result, unpack it

        #check the password
        if password == db_password:
            #check if user is a manager
            cursor.execute("SELECT * FROM Manager WHERE user_id=%s", (user_id,))
            if cursor.fetchone():
                cursor.close()
                conn.close()
                return render_template("manager.html", type=type) #manager page, opens the manager page
            else:
                cursor.close()
                conn.close()
                return render_template("restaurants.html", type=type)
        else:
            flash("Incorrect password.")
            cursor.close()
            conn.close()
            return render_template("login.html")
        
    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        first_name = request.form["name"]
        last_name = request.form["surname"]

                

        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="your_unique_db_pass",
            database="project"
        )
        cursor = conn.cursor()

        # Check if username already exists
        cursor.execute("SELECT * FROM User WHERE username=%s", (username,))
        if cursor.fetchone():
            flash("Username already exists. Please choose another one.")
            cursor.close()
            conn.close()            @app.route("/login", methods=["GET", "POST"])
            def login():
                if request.method == "POST":
                    username = request.form["username"]
                    password = request.form["password"]
                    conn = mysql.connector.connect(
                        host="localhost",
                        user="root",
                        password="your_unique_db_pass",
                        database="project"
                    )
                    cursor = conn.cursor()
                    # Check if the username exists
                    cursor.execute("SELECT user_id, password FROM User WHERE username=%s", (username,))
                    result = cursor.fetchone()
            
                    if not result:
                        flash("Username not found. Please register first.")
                        cursor.close()
                        conn.close()
                        return render_template("login.html")
                    user_id, db_password = result
                    if password == db_password:
                        # Check if user is a customer
                        cursor.execute("SELECT * FROM Customer WHERE user_id=%s", (user_id,))
                        if cursor.fetchone():
                            cursor.close()
                            conn.close()
                            return redirect(url_for("restaurants"))  # Redirect to restaurant selection page
                        # Check if user is a manager
                        cursor.execute("SELECT * FROM Manager WHERE user_id=%s", (user_id,))
                        if cursor.fetchone():
                            cursor.close()
                            conn.close()
                            return redirect(url_for("manager_dashboard"))  # Replace with your manager page
                        # If user is neither
                        flash("User role not found.")
                        cursor.close()
                        conn.close()
                        return render_template("login.html")
                    else:
                        flash("Incorrect password.")
                        cursor.close()
                        conn.close()
                        return render_template("login.html")
                return render_template("login.html")
            return render_template("register.html")
        
        # Generate a new user_id
        cursor.execute("SELECT user_id FROM User ORDER BY user_id DESC LIMIT 1")
        last_user = cursor.fetchone()
        if last_user and last_user[0]:
            last_num = int(last_user[0][1:])  # skip 'U'
            user_id = f"U{last_num+1:03d}" #increment
        else:
            user_id = "U001"

        # Insert into User table
        cursor.execute(
            "INSERT INTO User (user_id, username, password, first_name, last_name) VALUES (%s, %s, %s, %s, %s)",
            (user_id, username, password, first_name, last_name)
        )
        # Insert into Customer table
        cursor.execute(
            "INSERT INTO Customer (user_id, signup_date) VALUES (%s, %s)",
            (user_id, datetime.now())
        )

        conn.commit()
        cursor.close()
        conn.close()
        flash("Registration successful! Please log in.")
        return redirect(url_for("login"))
    return render_template("register.html")

if __name__ == "__main__":
    app.run(debug=True)
