import mysql.connector


class DB:
    def __init__(self, host, user, pw, db):
        self.conn = mysql.connector.connect(
            host=host, user=user, password=pw, database=db
        )

    def getAllCustomer(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM Customer")
        executedQuery = cursor.fetchall()
        cursor.close()
        self.conn.close()
        return executedQuery