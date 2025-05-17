import mysql.connector

class DB:

    def __init__(self, pw, db):
        self.conn = mysql.connector.connect(
            host="localhost", user="root", password=pw, database=db, use_pure=False
        )

    def getAllCustomer(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM Customer")
        executedQuery = cursor.fetchall()
        cursor.close()
        self.conn.close()
        return executedQuery   # always return query

    def getUsername(self, emp_id):
        # get a real prepared cursor
        cur = self.conn.cursor(prepared=True)
        # NOTE: mysql.connector always uses %s placeholders
        sql = "SELECT username FROM User WHERE user_id = %s"
        cur.execute(sql, (emp_id,))
        row = cur.fetchone()
        cur.close()
        # return the actual value instead of the SQL string
        return row

