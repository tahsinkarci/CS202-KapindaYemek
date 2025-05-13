from flask import Flask, render_template
import mysql.connector
import mysql.connector
print("Connector is working!")


app = Flask(__name__)

@app.route("/")
def home():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="tHfB1848*D2#",               #(#) yorummus, enter YOUR db password
        database="homework"
    )
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Customer")
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template("index.html", data=data)

if __name__ == "__main__":
    app.run(debug=True)
