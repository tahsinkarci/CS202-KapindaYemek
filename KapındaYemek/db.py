import mysql.connector
from datetime import datetime


class db:

    def __init__(self, pw, db):
        self.conn = mysql.connector.connect(
            host="localhost", user="root", password=pw, database=db, use_pure=True
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
        cursor.execute("SELECT restaurant_id "
                       "FROM restaurant "
                       "WHERE name=%s", (name,))
        result = cursor.fetchone()
        cursor.close()
        return result[0] if result else None  # just the ID, not a tuplereturn result

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
        cursor.execute("SELECT m.name,m.price "
                       "FROM restaurant r "
                       "JOIN offers o ON r.restaurant_id = o.restaurant_id "
                       "JOIN menuitem m ON o.menu_item_id  = m.menu_item_id "
                       "WHERE r.name = %s", (name))
        self.conn.commit()
        data = cursor.fetchall()
        cursor.close()
        return data
    
    def getMenuByRestaurantName(self, restaurant_name):
        cursor = self.conn.cursor()
        #first, get the restaurant_id for the given restaurant_name
        cursor.execute("SELECT restaurant_id FROM Restaurant WHERE name = %s", (restaurant_name,))
        res = cursor.fetchone()
        if not res:
            cursor.close()
            return []
        restaurant_id = res[0]

        #second, get menu items offered by this restaurant by using offers and menuitem tables
        cursor.execute("""
            SELECT m.menu_item_id, m.name, m.description, m.price
            FROM MenuItem m
            JOIN offers o ON m.menu_item_id = o.menu_item_id
            WHERE o.restaurant_id = %s
        """, (restaurant_id,))
        menu_items = cursor.fetchall()
        cursor.close()
        return menu_items

    def getLastCartID(self):
        cursor = self.conn.cursor(prepared=True)
        cursor.execute("SELECT cart_id FROM Cart ORDER BY cart_id DESC LIMIT 1")
        result = cursor.fetchone()
        cursor.close()
        return result[0] if result else None

    def get_last_cart_id(self):
        """
        Returns the last (highest) cart_id from the Cart table, or None if no carts exist.
        """
        cursor = self.conn.cursor()
        query = "SELECT cart_id FROM Cart ORDER BY cart_id DESC LIMIT 1"
        cursor.execute(query)
        result = cursor.fetchone()
        return result[0] if result else None

    def getLastSaleID(self):
        cursor = self.conn.cursor(prepared=True)
        cursor.execute("SELECT sale_id FROM sales ORDER BY sale_id DESC LIMIT 1")
        result = cursor.fetchone()
        cursor.close()
        return result[0] if result else None

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

    def update_cart_status(self, cart_id, status):
        cursor = self.conn.cursor()
        cursor.execute("UPDATE Cart SET status = %s WHERE cart_id = %s", (status, cart_id))
        self.conn.commit()
        cursor.close()

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

    def addMenuItemToCart(self, cart_id, menu_item_id, quantity):  # in menu page the total am. needs to be calculated
        cursor = self.conn.cursor(prepared=True)        # her bir menu item listeye eklenince tek tek kullanılmalı
        cursor.execute(
            "INSERT INTO contains (cart_id, menu_item_id, quantity) VALUES (%s, %s, %s)",
            (cart_id, menu_item_id, quantity)
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
        cursor.execute(sql, (discount_id,))
        self.conn.commit()
        data = cursor.fetchall()
        cursor.close()
        return data

    ##### sales page methods #####

    def createSale(self, sale_id, status, price):
        cursor = self.conn.cursor(prepared=True)
        sql = "INSERT INTO Sales(sale_id, status, price) " \
              "VALUES (%s, %s, %s)"
        cursor.execute(sql, (sale_id, status, price))
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

    def create_places_relation(self, sale_id, cart_id):
        cursor = self.conn.cursor()
        sql = "INSERT INTO places (sale_id, cart_id) VALUES (%s, %s)"
        cursor.execute(sql, (sale_id, cart_id))
        self.conn.commit()
        cursor.close()

    def createReceivesRelation(self, cart_id, restaurant_id):
        cursor = self.conn.cursor(prepared=True)
        sql = "INSERT INTO receives(cart_id, restaurant_id) " \
              "VALUES (%s, %s)"
        cursor.execute(sql, (cart_id, restaurant_id))
        self.conn.commit()
        data = cursor.fetchall()
        cursor.close()
        return data

    def createMakesRelation(self, sale_id, user_id, date=datetime.now()):
        cursor = self.conn.cursor(prepared=True)
        sql = "INSERT INTO makes(sale_id, user_id, date) " \
              "VALUES (%s, %s, %s)"
        cursor.execute(sql, (sale_id, user_id, date))
        self.conn.commit()
        data = cursor.fetchall()
        cursor.close()
        return data

    def create_make_relation(self, sale_id, user_id, date=None):
        from datetime import datetime
        if date is None:
            date = datetime.now()
        cursor = self.conn.cursor()
        sql = "INSERT INTO makes (sale_id, user_id, date) VALUES (%s, %s, %s)"
        cursor.execute(sql, (sale_id, user_id, date))
        self.conn.commit()
        cursor.close()

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
        cursor.execute("SELECT  DISTINCT  s.sale_id, s.price, s.status, m.date "
                       "FROM sales s "
                       "JOIN makes m ON s.sale_id = m.sale_id "
                       "JOIN checks c ON s.sale_id = c.sale_id "
                       "JOIN manages ma ON c.user_id = ma.user_id "
                       "WHERE c.user_id = %s ORDER BY s.sale_id", (user_id,))
        data = cursor.fetchall()
        cursor.close()
        return data

    def getRestaurantManagerIDByName(self, namee):
        cursor = self.conn.cursor(prepared=True)
        cursor.execute("SELECT user_id FROM manages m "
                       "JOIN restaurant r ON r.restaurant_id = m.restaurant_id "
                       "WHERE r.name = %s", (namee,))
        result = cursor.fetchone()
        cursor.close()
        return result[0] if result else None


############ Discounts ######################
    def create_discount(self, menu_item_id, amount, start_date, finish_date):
        cur = self.conn.cursor()
        # generate next discount_id like D001
        cur.execute("SELECT MAX(discount_id) FROM Discount")
        last = cur.fetchone()[0]
        next_id = f"D{int(last[1:]) + 1:03d}" if last else "D001"

        cur.execute("""
            INSERT INTO Discount (discount_id, menu_item_id, start_date, finish_date, amount)
            VALUES (%s, %s, %s, %s, %s)
        """, (next_id, menu_item_id, start_date, finish_date, amount))

        self.conn.commit()
        cur.close()

    def getAllMenuItems(self):
        cur = self.conn.cursor()
        cur.execute("SELECT menu_item_id, name FROM MenuItem")
        return cur.fetchall()

    def getMenuWithDiscounts(self, restaurant_name):
        cur = self.conn.cursor()
        cur.execute("""
            SELECT 
                m.menu_item_id,
                m.name,
                m.description,
                m.price,
                d.amount,
                d.start_date,
                d.finish_date
            FROM MenuItem m
            JOIN offers o ON o.menu_item_id = m.menu_item_id
            JOIN Restaurant r ON r.restaurant_id = o.restaurant_id
            LEFT JOIN Discount d
                ON d.menu_item_id = m.menu_item_id
               AND d.start_date <= NOW()
               AND d.finish_date >= NOW()
            WHERE r.name = %s
        """, (restaurant_name,))
        return cur.fetchall()

    def getMenuItemsByManager(self, user_id):
        cur = self.conn.cursor()
        cur.execute("""
            SELECT m.menu_item_id, m.name
            FROM MenuItem m
            JOIN offers o        ON o.menu_item_id = m.menu_item_id
            JOIN Restaurant r    ON r.restaurant_id = o.restaurant_id
            JOIN Manages mg      ON mg.restaurant_id = r.restaurant_id
            WHERE mg.user_id = %s
        """, (user_id,))
        return cur.fetchall()

    def get_approved_carts_by_user(self, user_id):
        cursor = self.conn.cursor()
        query = """
            SELECT c.cart_id, c.status, c.total_amount
            FROM Cart c
            JOIN Approves a ON c.cart_id = a.cart_id
            WHERE a.user_id = %s AND c.status = 'approved'
        """
        cursor.execute(query, (user_id,))
        return cursor.fetchall()

    def addApprove(self, cart_id, user_id):
        cursor = self.conn.cursor()
        sql = "INSERT INTO approves (user_id, cart_id) VALUES (%s, %s)"
        cursor.execute(sql, (user_id, cart_id))
        self.conn.commit()
        cursor.close()

    def get_paid_carts_by_user(self, user_id):
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT p.cart_id, s.price, m.date
            FROM Sales s
            JOIN makes m ON s.sale_id = m.sale_id
            JOIN places p ON s.sale_id = p.sale_id
            WHERE m.user_id = %s AND s.status = 'pending'
            ORDER BY m.date DESC
        """, (user_id,))
        carts = cursor.fetchall()
        cursor.close()
        return carts

    def get_accepted_carts_by_user(self, user_id):
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT p.cart_id, s.price, m.date
            FROM Sales s
            JOIN makes m ON s.sale_id = m.sale_id
            JOIN places p ON s.sale_id = p.sale_id
            WHERE m.user_id = %s AND s.status = 'accepted'
            ORDER BY m.date DESC
        """, (user_id,))
        carts = cursor.fetchall()
        cursor.close()
        return carts

    def get_past_carts_by_user(self, user_id):
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT p.cart_id, s.price, m.date, s.status
            FROM Sales s
            JOIN makes m ON s.sale_id = m.sale_id
            JOIN places p ON s.sale_id = p.sale_id
            WHERE m.user_id = %s AND s.status IN ('cancelled', 'closed')
            ORDER BY m.date DESC
        """, (user_id,))
        carts = cursor.fetchall()
        cursor.close()
        return carts

    def get_cart_amount(self, cart_id):
        cursor = self.conn.cursor()
        cursor.execute("SELECT total_amount FROM Cart WHERE cart_id = %s", (cart_id,))
        result = cursor.fetchone()
        cursor.close()
        return result[0] if result else 0

    def add_rating(self, rating_id, rating, comment, restaurant_id):
        cursor = self.conn.cursor()
        sql = "INSERT INTO rating (rating_id, star, comment, restaurant_id) VALUES (%s, %s, %s, %s)"
        cursor.execute(sql, (rating_id, rating, comment, restaurant_id))
        self.conn.commit()
        cursor.close()

    def create_leaves_relation(self, rating_id, user_id):
        cursor = self.conn.cursor()
        sql = "INSERT INTO leaves (rating_id, user_id) VALUES (%s, %s)"
        cursor.execute(sql, (rating_id, user_id))
        self.conn.commit()
        cursor.close()

    def get_latest_rating_id(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT rating_id FROM rating ORDER BY rating_id DESC LIMIT 1")
        result = cursor.fetchone()
        cursor.close()
        return result[0] if result else None

    def getRestaurantIDByCartID(self, cart_id):
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT r.restaurant_id
            FROM Cart c
            JOIN contains co ON c.cart_id = co.cart_id
            JOIN MenuItem m ON co.menu_item_id = m.menu_item_id
            JOIN offers o ON m.menu_item_id = o.menu_item_id
            JOIN Restaurant r ON o.restaurant_id = r.restaurant_id
            WHERE c.cart_id = %s
            LIMIT 1
        """, (cart_id,))
        result = cursor.fetchone()
        cursor.close()
        return result[0] if result else None


