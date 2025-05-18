import mysql.connector

class DB:

    def __init__(self, pw, db):
        self.conn = mysql.connector.connect(
            host="localhost", user="root", password=pw, database=db, use_pure=False
        )

    def getUsernameByID(self, id):  # giver user id (customer or admin)
        # get a real prepared cursor
        cur = self.conn.cursor(prepared=True)
        # NOTE: mysql.connector always uses %s placeholders
        sql = "SELECT username FROM User WHERE user_id = %s"
        cur.execute(sql, (id,))
        row = cur.fetchone()
        cur.close()
        # return the actual value instead of the SQL string
        return row

    def getPasswordByID(self, id):
        cur = self.conn.cursor(prepared=True)
        # NOTE: mysql.connector always uses %s placeholders
        sql = "SELECT password FROM User WHERE id = %s"
        cur.execute(sql, (id,))
        row = cur.fetchone()
        cur.close()
        return row

    def getAllRestaurants(self):
        cur = self.conn.cursor(prepared=True)
        # NOTE: mysql.connector always uses %s placeholders
        cur.execute("SELECT name FROM Restaurant")
        rows = cur.fetchall()
        cur.close()
        return [r[0] for r in rows]

    def getRestaurantByName(self, name):
        cur = self.conn.cursor(prepared=True)
        sql = "SELECT id FROM Restaurant WHERE name = %s"
        cur.execute(sql, (name,))
        row = cur.fetchone()
        cur.close()
        return row

    def createMenuItem(self, menu_item_id, name, description, price, restaurant_id):
        cur = self.conn.cursor(prepared=True)
        sql = sql = """
            INSERT INTO MenuItems (menu_item_id, name, description, price, restaurant_id)
            VALUES (%s, %s, %s, %s, %s)
        """
        cur.execute(sql, (menu_item_id, name, description, price, restaurant_id))
        row = cur.fetchone()
        cur.close()
        return row

    def getMenuItemByName(self, name):
        cur = self.conn.cursor(prepared=True)
        sql = "SELECT id FROM MenuItem WHERE name = %s"
        cur.execute(sql, (name,))
        row = cur.fetchone()
        cur.close()
        return row

    def deleteMenuItemByID(self, id):
        cur = self.conn.cursor(prepared=True)
        sql = "DELETE FROM MenuItems WHERE menu_item_id = %s"
        cur.execute(sql, (id,))
        row = cur.fetchone()
        cur.close()
        return row