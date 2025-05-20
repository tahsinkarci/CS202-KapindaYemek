from flask import Flask, render_template, request, redirect, url_for, flash, session
from db import db
from datetime import datetime

print("Connector is working!")

## enter your db password here 
databaseConnection = db("tHfB1848*D2#", "project")  # the constructor itself creates connection


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

        #delete selected items from cart
        elif action == "delete":
            for item_id in selected_items:
                session["cart"].pop(item_id, None)
            flash("Selected items removed from cart.")

        #increment item count
        elif action == "plus" and item_id:
            if item_id in session["cart"]:
                session["cart"][item_id] += 1

        #decrement item count, min. 1
        elif action == "minus" and item_id:
            if item_id in session["cart"] and session["cart"][item_id] > 1:
                session["cart"][item_id] -= 1

        #approve cart
        elif action == "approve":
            total_amount = 0
            for item in menu_list:
                item_id_str = str(item[0])
                if item_id_str in session["cart"]:
                    quantity = session["cart"][item_id_str]
                    total_amount += float(item[3]) * int(quantity)

            # Generate a new cart_id like C001, C002, ...
            last_cart_id = databaseConnection.get_last_cart_id()  #take the last cart id
            if last_cart_id:
                last_num = int(last_cart_id[1:])
                cart_id = f"C{last_num + 1:03d}"
            else:
                cart_id = "C001"

            databaseConnection.createCart(cart_id, "approved", total_amount)

            #add each menu item and its count to the cart
            for item in menu_list:
                item_id_str = str(item[0])
                if item_id_str in session["cart"]:
                    quantity = session["cart"][item_id_str]
                    databaseConnection.addMenuItemToCart(cart_id, item_id_str, quantity) #add menu cart relationship

            # Add Approves record
            user_id = session.get("user_id")
            databaseConnection.addApprove(cart_id, user_id)

            flash(f"Cart approved! (Cart ID: {cart_id}, Total: ${total_amount})")
            session["cart"] = {}

        elif action == "pay":
            
            session.modified = True
            return redirect(url_for("pay"))  # Redirect to pay.html

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
    total_sales = sum(sale[1] for sale in sales_list
                      if sale[1] is not None ) if sales_list else 0  #sale[1] is the amount

    #calculate monthly sales as well
    now = datetime.now()
    monthly_sales = sum(
        sale[1] for sale in sales_list
        if sale[1] is not None
        if sale[1] is not None
        if sale[3].month == now.month and sale[3].year == now.year #check the time of the sale, sale[3] is the date
    ) if sales_list else 0  

    return render_template(
        "manager.html",
        sales=sales_list,
        total_sales=total_sales,
        monthly_sales=monthly_sales
    )

@app.route("/pay", methods=["GET", "POST"])
def pay():
    user_id = session.get("user_id")
    if request.method == "POST":
        selected_carts = request.form.getlist("selected_carts")
        if selected_carts:
            for cart_id in selected_carts:
                databaseConnection.update_cart_status(cart_id, "paid")
            flash(f"{len(selected_carts)} cart(s) marked as paid.")
        else:
            flash("No carts selected.")
        return redirect(url_for("pay"))

    approved_carts = databaseConnection.get_approved_carts_by_user(user_id)
    return render_template("pay.html", carts=approved_carts)


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

    user_id = session.get("user_id")
    menu_items = databaseConnection.getMenuItemsByManager(user_id)

    return render_template("discounts.html", menu_items=menu_items)



if __name__ == "__main__":
    app.run(debug=True)