import psycopg2

class DataBaseService:
    def __init__(self):
        self.conn = psycopg2.connect(database="technopark", user="postgres", password="12345", host="127.0.0.1",
                                     port="5432")
        self.cur = self.conn.cursor()

    def reconnect(self):
        self.conn.close()
        self.conn = psycopg2.connect(database="technopark", user="postgres", password="12345", host="127.0.0.1",
                                     port="5432")
        self.cur = self.conn.cursor()

    def execute(self, cmd):
        self.cur.execute(cmd)
        self.conn.commit()

    def get_result(self):
        return self.cur.fetchall()

    def close(self):
        self.conn.close()

db_service = DataBaseService()
