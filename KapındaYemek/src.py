from flask import Flask, render_template
from flask import request, redirect, url_for, flash
import mysql.connector
import mysql.connector
print("Connector is working!")


app = Flask(__name__)
app.secret_key = "asdasfamanasqwezayras"  # Add this line

@app.route("/")
def home():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="tHfB1848*D2#",  # enter YOUR db password
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
            password="tHfB1848*D2#",
            database="project"
        )
        cursor = conn.cursor()
        # first, check if the username exists
        cursor.execute("SELECT password FROM User WHERE username=%s", (username,))
        result = cursor.fetchone()

        if not result:
            flash("Username not found. Please register first.")
            cursor.close()
            conn.close()
            return render_template("login.html")
        # If username exists, check password
        db_password = result[0]
        if password == db_password:
            cursor.close()
            conn.close()
            return redirect(url_for("home"))
        else:
            flash("Incorrect password.")
            cursor.close()
            conn.close()
            return render_template("login.html")
    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # Registration logic goes here
        flash("Registration is not implemented yet.")
        return redirect(url_for("login"))
    return render_template("register.html")

if __name__ == "__main__":
    app.run(debug=True)
