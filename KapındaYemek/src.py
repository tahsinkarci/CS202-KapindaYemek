from flask import Flask, render_template
import mysql.connector
from DB import DB

print("Connector is working!")


app = Flask(__name__)

@app.route("/")
def home():
    connection = DB("#123321#%&", "homework")

     #data = connection.getAllCustomer()
    data = connection.getUsername("C1")


    return render_template("index.html", data=data)

if __name__ == "__main__":
    app.run(debug=True)
