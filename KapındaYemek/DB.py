import mysql.connector

class DB:

    def __init__(self, pw, db):
        self.conn = mysql.connector.connect(
            host="localhost", user="root", password=pw, database=db, use_pure=False
        )

    def getUsername(self, id):  # giver user id (customer or admin)
        # get a real prepared cursor
        cur = self.conn.cursor(prepared=True)
        # NOTE: mysql.connector always uses %s placeholders
        sql = "SELECT username FROM User WHERE user_id = %s"
        cur.execute(sql, (id,))
        row = cur.fetchone()
        cur.close()
        # return the actual value instead of the SQL string
        return row

    def getPassword(self, pswd):
        cur = self.conn.cursor(prepared=True)
        # NOTE: mysql.connector always uses %s placeholders
        sql = "SELECT password FROM User WHERE password = %s"
        cur.execute(sql, (pswd,))
        row = cur.fetchone()
        cur.close()
        return row
