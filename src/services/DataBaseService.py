import psycopg2
import psycopg2.extras

class DataBaseService:
    def __init__(self):
        self.conn = psycopg2.connect(database="technopark", user="postgres", password="12345", host="127.0.0.1",
                                     port="5432")
        self.cur = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    def reconnect(self):
        self.conn.close()
        self.conn = psycopg2.connect(database="technopark", user="postgres", password="12345", host="127.0.0.1",
                                     port="5432")
        self.cur = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    def execute(self, cmd):
        self.cur.execute(cmd)
        self.conn.commit()

    def get_all(self):
        return self.cur.fetchall()

    def get_one(self):
        return self.cur.fetchone()

    def close(self):
        self.conn.close()

db_service = DataBaseService()
