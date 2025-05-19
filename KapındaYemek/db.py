import mysql.connector
from datetime import datetime


class db:

    def __init__(self, pw, db):
        self.conn = mysql.connector.connect(
            host="localhost", user="root", password=pw, database=db, use_pure=False
        )


    def get_user_by_username(self,username):
        cursor = self.conn.cursor(prepared=True)
        cursor.execute("SELECT user_id, password FROM User WHERE username=%s", (username,))
        result = cursor.fetchone()
        cursor.close()
        return result

    def getIDByUsername(self,username):
        cursor = self.conn.cursor(prepared=True)
        cursor.execute("SELECT user_id FROM User WHERE username=%s", (username,))
        result = cursor.fetchone()
        cursor.close()
        return result

    def username_exists(self,username):
        cursor = self.conn.cursor(prepared=True)
        cursor.execute("SELECT 1 FROM User WHERE username=%s", (username,))
        exists = cursor.fetchone() is not None
        cursor.close()
        return exists

    def is_manager(self,user_id):
        cursor = self.conn.cursor(prepared=True)
        cursor.execute("SELECT * FROM Manager WHERE user_id=%s", (user_id,))
        result = cursor.fetchone()
        cursor.close()
        return result is not None

    def is_customer(self,user_id):
        cursor = self.conn.cursor(prepared=True)
        cursor.execute("SELECT * FROM Customer WHERE user_id=%s", (user_id,))
        result = cursor.fetchone()
        cursor.close()
        return result is not None

    def get_last_user_id(self):
        cursor = self.conn.cursor(prepared=True)
        cursor.execute("SELECT user_id FROM User ORDER BY user_id DESC LIMIT 1")
        result = cursor.fetchone()
        cursor.close()
        return result[0] if result else None

    def get_last_customer_id(self):
        cursor = self.conn.cursor(prepared=True)
        cursor.execute("SELECT customer_id FROM Customer ORDER BY customer_id DESC LIMIT 1")
        result = cursor.fetchone()
        cursor.close()
        return result[0] if result else None

    def insert_user(self,user_id, username, password, first_name, last_name):
        cursor = self.conn.cursor(prepared=True)
        cursor.execute(
            "INSERT INTO User (user_id, username, password, first_name, last_name) VALUES (%s, %s, %s, %s, %s)",
            (user_id, username, password, first_name, last_name)
        )
        cursor.commit()
        cursor.close()

    def insert_customer(self,customer_id, user_id):
        cursor = self.conn.cursor(prepared=True)
        cursor.execute(
            "INSERT INTO Customer (customer_id, user_id, signup_date) VALUES (%s, %s, %s)",
            (customer_id, user_id, datetime.now())
        )
        cursor.commit()
        cursor.close()


    def get_all_customers(self):
        cursor = self.conn.cursor(prepared=True)
        cursor.execute("SELECT * FROM Customer")
        data = cursor.fetchall()
        cursor.close()
        return data

############# Restaurant selection page Methods ######################

    def getRestaurantByName(self,name): # to get selected restaurant (when going next page)
        cursor = self.conn.cursor(prepared=True)
        cursor.execute("SELECT restaurant_id FROM restaurant WHERE name=%s", (name,))
        result = cursor.fetchone()
        cursor.close()
        return result

    def getAllRestaurants(self): # to list restaurant
        cursor = self.conn.cursor(prepared=True)
        cursor.execute("SELECT name FROM restaurant ORDER BY name")
        data = cursor.fetchall()
        cursor.close()
        return [r[0] for r in data]

############# Menu selection page Methods ######################

    #o restaurant in bütün menuitemlerini {name, price} şeklinde döndürür
    def listAllMenuItemsByNameOfRestaurantWithPrice(self, name): # workbenchte calısıo
        cursor = self.conn.cursor(prepared=True)
        cursor.execute("SELECT m.name,m.price"
                        "FROM restaurant r"
                        "JOIN offers o ON r.restaurant_id = o.restaurant_id"
                        "JOIN menuitem m ON o.menu_item_id  = m.menu_item_id"
                        "WHERE r.name = %s", (name))
        self.conn.commit()
        data = cursor.fetchall()
        cursor.close()
        return data

    def createCart(self, cart_id, status, total_amount):  # in menu page the total am. needs to be calculated,
        cursor = self.conn.cursor(prepared=True)          # then cart has to be created
        cursor.execute("INSERT INTO Cart (cart_id, status, created_at, updated_at, total_amount)"
                       " VALUES (%s, %s, %s,%s, %s)",
            (cart_id, status, datetime.now(), datetime.now(), total_amount))
        self.conn.commit()
        data = cursor.fetchall()
        cursor.close()

        return data

    def updateCart(self, cart_id,  total_amount):
        cursor = self.conn.cursor(prepared=True)
        cursor.execute(
            "UPDATE Cart SET status = 'pending', updated_at = %s, total_amount = %s WHERE cart_id = %s",
            ( datetime.now(), total_amount, cart_id)
        )
        self.conn.commit()
        updated = cursor.rowcount
        cursor.close()
        return updated

    def deleteCart(self, cart_id):
        cursor = self.conn.cursor(prepared=True)
        cursor.execute(
            "DELETE FROM Cart WHERE cart_id = %s",
            (cart_id,)
        )
        self.conn.commit()
        deleted = cursor.rowcount
        cursor.close()
        return deleted

    def addMenuItemToCart(self, cart_id, menu_item_id):  # in menu page the total am. needs to be calculated
        cursor = self.conn.cursor(prepared=True)        # her bir menu item listeye eklenince tek tek kullanılmalı
        cursor.execute(
            "INSERT INTO contains (cart_id, menu_item_id) VALUES (%s, %s)",
            (cart_id, menu_item_id)
        )
        self.conn.commit()
        data = cursor.fetchall()
        cursor.close()
        return data

    def removeMenuItemFromCart(self, cart_id, menu_item_id):
        cursor = self.conn.cursor(prepared=True)
        cursor.execute(
            "DELETE FROM contains WHERE cart_id = %s AND menu_item_id = %s",
            (cart_id, menu_item_id)
        )
        self.conn.commit()
        data = cursor.fetchall()
        cursor.close()
        return data

############# Paying page Methods ######################
    def createDiscount(self,discount_id,menu_item_id, finis_date, amount):
        cursor = self.conn.cursor(prepared=True)
        sql = "INSERT INTO Discount(discount_id, menu_item_id, start_date, finish_date, amount) " \
              "VALUES (%s, %s, %s, %s, %s)"

        cursor.execute(sql, (discount_id,menu_item_id, datetime.now(), finis_date, amount))
        self.conn.commit()
        data = cursor.fetchall()
        cursor.close()
        return data

    def deleteDiscount(self,discount_id):
        cursor = self.conn.cursor(prepared=True)
        sql = "DELETE FROM Discount WHERE discount_id = %s",
        cursor.execute(sql, (discount_id))
        self.conn.commit()
        data = cursor.fetchall()
        cursor.close()
        return data

    ##### sales page methods #####

    def createSale(self, sale_id, status, price):
        cursor = self.conn.cursor(prepared=True)
        sql = "INSERT INTO Sales(sale_id, cart_id, customer_id, restaurant_id, total_amount) " \
              "VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(sql, (sale_id, cart_id, customer_id, restaurant_id, total_amount))
        self.conn.commit()
        data = cursor.fetchall()
        cursor.close()
        return data

    def getAllSales(self):
        cursor = self.conn.cursor(prepared=True)
        cursor.execute( "SELECT s.sale_id,\n"
        "       s.price,\n"
        "       s.status,\n"
        "       m.date,\n"
        "       m.user_id AS customer_id\n"
        "  FROM sales s\n"
        "  JOIN makes m ON s.sale_id = m.sale_id\n"
        " ORDER BY s.sale_id")
        data = cursor.fetchall()
        cursor.close()
        return data


    def updateSale(self, sale_id, status):
        cursor = self.conn.cursor(prepared=True)
        sql = "UPDATE Sales SET status = %s WHERE sale_id = %s"
        cursor.execute(sql, (status, sale_id))
        self.conn.commit()
        data = cursor.fetchall()
        cursor.close()
        return data

    def deleteSale(self, sale_id):
        cursor = self.conn.cursor(prepared=True)
        sql = "DELETE FROM Sales WHERE sale_id = %s"
        cursor.execute(sql, (sale_id,))
        self.conn.commit()
        data = cursor.fetchall()
        cursor.close()
        return data

    def createPlacesRelation(self,sale_id, cart_id):
        cursor = self.conn.cursor(prepared=True)
        sql = "INSERT INTO places(sale_id, cart_id) " \
              "VALUES (%s, %s)"
        cursor.execute(sql, (sale_id, cart_id))
        self.conn.commit()
        data = cursor.fetchall()
        cursor.close()
        return data

    def createCheck(self, sale_id, user_id):
        cursor = self.conn.cursor(prepared=True)
        sql = "INSERT INTO checks(sale_id, user_id) " \
              "VALUES (%s, %s)"
        cursor.execute(sql, (sale_id, user_id))
        self.conn.commit()
        data = cursor.fetchall()
        cursor.close()
        return data

    def deleteCheck(self, sale_id):
        cursor = self.conn.cursor(prepared=True)
        sql = "DELETE FROM checks WHERE sale_id = %s"
        cursor.execute(sql, (sale_id,))
        self.conn.commit()
        data = cursor.fetchall()
        cursor.close()
        return data
    def deleteSale(self, sale_id):
        cursor = self.conn.cursor(prepared=True)
        sql = "DELETE FROM Sales WHERE sale_id = %s"
        cursor.execute(sql, (sale_id,))
        self.conn.commit()
        data = cursor.fetchall()
        cursor.close()
        return data

    def getAllchecks(self):
        cursor = self.conn.cursor(prepared=True)
        cursor.execute("SELECT * FROM checks")
        self.conn.commit()
        data = cursor.fetchall()
        cursor.close()
        return data

    def getRestaurantManagerByID(self, user_id):
        cursor = self.conn.cursor(prepared=True)
        cursor.execute("SELECT s.sale_id, s.price, s.status, m.date "
                       "FROM sales s "
                       "JOIN makes m ON s.sale_id = m.sale_id "
                       "JOIN checks c ON s.sale_id = c.sale_id "
                       "WHERE c.user_id = %s ORDER BY s.sale_id", (user_id,))
        data = cursor.fetchall()
        cursor.close()
        return data