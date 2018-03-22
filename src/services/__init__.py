import psycopg2

conn = psycopg2.connect(database="technopark", user="postgres", password="12345", host="127.0.0.1", port="5432")

cur = conn.cursor()