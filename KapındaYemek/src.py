from flask import Flask, render_template, request, redirect, url_for, flash, session
from db import db
from datetime import datetime

print("Connector is working!")

## enter your db password here
databaseConnection = db("#123321#%&", "project")  # the constructor itself creates connection


app = Flask(__name__)
app.secret_key = "asdasfamanasqwezayras"


@app.route("/")
def home():

    return render_template("home.html")

#LOGIN PAGE################################################################################
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        result = databaseConnection.get_user_by_username(username)
        userid = databaseConnection.getIDByUsername(username)  # keeps selected user id

        if not result:
            flash("Username not found. Please register first.")
            return render_template("login.html")

        # if result is not None:
        user_id, db_password = result
        session["user_id"] = user_id
        if password == db_password:
            if databaseConnection.is_manager(user_id):
                # type = "manager"
                return redirect(url_for("manager"))  # you can add type
            else:
                # type = "customer"
                return redirect(url_for("selectRestaurant"))  # you can add type
        else:
            flash("Incorrect password.")
            return render_template("login.html")
    return render_template("login.html")

#REGISTER PAGE################################################################################
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        first_name = request.form["name"]
        last_name = request.form["surname"]

        if databaseConnection.username_exists(username):
            flash("Username already exists. Please choose another one.")
            return render_template("register.html")

        # Generate a new user_id
        last_user_id = databaseConnection.get_last_user_id()
        if last_user_id:
            last_num = int(last_user_id[1:])
            user_id = f"U{last_num + 1:03d}"
        else:
            user_id = "U001"

        databaseConnection.insert_user(user_id, username, password, first_name, last_name)
        databaseConnection.insert_customer(user_id)
        flash("Registration successful! Please log in.")

        return redirect(url_for("login"))
    return render_template("register.html")
#RESTAURANT PAGE################################################################################
@app.route("/selectRestaurant", methods=["GET", "POST"])
def selectRestaurant():
    if request.method == "POST":
        selected_restaurant = request.form.get("restaurant")
        flash(f"You selected: {selected_restaurant}")
        # You can redirect to another page or process the selection here
        return redirect(url_for("menu", restaurant_name=selected_restaurant))

    #then it is get
    restaurant_list = databaseConnection.getAllRestaurants()
    return render_template("restaurants.html", restaurant_names=restaurant_list)

#MENU PAGE################################################################################
@app.route("/menu.html", methods=["GET", "POST"])
def menu():
    restaurant_name = request.args.get("restaurant_name") or session.get("restaurant_name")
    if restaurant_name:
        session["restaurant_name"] = restaurant_name
    else:
        flash("No restaurant selected.")
        return redirect(url_for("selectRestaurant"))

    menu_list = databaseConnection.getMenuByRestaurantName(restaurant_name)

    #initialize cart if there is not
    if "cart" not in session or not isinstance(session["cart"], dict):
        session["cart"] = {}

    if request.method == "POST":
        action = request.form.get("action")
        selected_items = request.form.getlist("selected_items")
        item_id = request.form.get("item_id")  # for plus/minus

        #add selected items from menu to cart
        if action == "add":
            for item_id in selected_items:
                if item_id not in session["cart"]:
                    session["cart"][item_id] = 1
            flash("Selected items added to cart.")

        # Delete selected items from cart
        elif action == "delete":
            for item_id in selected_items:
                session["cart"].pop(item_id, None)
            flash("Selected items removed from cart.")

        # Increment item count
        elif action == "plus" and item_id:
            if item_id in session["cart"]:
                session["cart"][item_id] += 1

        # Decrement item count (minimum 1)
        elif action == "minus" and item_id:
            if item_id in session["cart"] and session["cart"][item_id] > 1:
                session["cart"][item_id] -= 1

        # Approve cart
        elif action == "approve":
            
            flash("Cart approved!)")
            session["cart"] = {}

        session.modified = True

    # Prepare cart items to display
    cart_items = []
    if session.get("cart"):
        for item in menu_list:
            item_id = str(item[0])
            if item_id in session["cart"]:
                quantity = session["cart"][item_id]
                # item = (id, name, desc, price)
                cart_items.append((item[0], item[1], item[2], float(item[3]), int(quantity)))

    return render_template(
        "menu.html",
        menu=menu_list,
        restaurant_name=restaurant_name,
        cart=cart_items
    )

#SALE PAGE################################################################################
@app.route("/update_sale_status", methods=["POST"])
def update_sale_status():

    decision = request.form.get("decision")  # cancel sale , reopen sale, accept sale, reject sale

    if decision == "Cancel Sale":
        sale_id = request.form.get("sale_id")
        databaseConnection.updateSale(sale_id, "cancelled")
    elif decision == "Reopen Sale":
         sale_id = request.form.get("sale_id")
         databaseConnection.updateSale(sale_id, "reopened")
    elif decision == "Accept":
        sale_id = request.form.get("sale_id")
        databaseConnection.updateSale(sale_id, "accepted")
    elif decision == "Reject":
        sale_id = request.form.get("sale_id")
        databaseConnection.updateSale(sale_id, "rejected")

    return redirect(url_for("manager"))



@app.route("/manager", methods=["GET"])
def manager():
    user_id = session.get("user_id")  # get the user_id from login page
    sales_list = databaseConnection.getRestaurantManagerByID(user_id)

    #total sales
    total_sales = sum(sale[1] for sale in sales_list
                      if sale[1] is not None ) if sales_list else 0  #sale[1] is the amount

    #calculate monthly sales as well
    now = datetime.now()
    monthly_sales = sum(
        sale[1] for sale in sales_list
        if sale[1] is not None
        if sale[3].month == now.month and sale[3].year == now.year #check the time of the sale, sale[3] is the date
    ) if sales_list else 0  

    return render_template(
        "manager.html",
        sales=sales_list,
        total_sales=total_sales,
        monthly_sales=monthly_sales
    )



@app.route("/manager/discounts", methods=["GET", "POST"])
def define_discounts():
    if request.method == "POST":
        menu_item_id = request.form["menu_item_id"]
        amount = request.form["amount"]
        start_date = request.form["start_date"]
        finish_date = request.form["finish_date"]

        databaseConnection.create_discount(menu_item_id, amount, start_date, finish_date)
        flash("Discount created successfully.")
        return redirect(url_for("define_discounts"))

    menu_items = databaseConnection.getAllMenuItems()
    return render_template("discounts.html", menu_items=menu_items)



if __name__ == "__main__":
    app.run(debug=True)