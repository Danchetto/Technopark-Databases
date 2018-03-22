import psycopg2

conn = psycopg2.connect(database="technopark", user="postgres", password="12345", host="127.0.0.1", port="5432")

cur = conn.cursor()

# db_create = open('../dbscheme.sql', 'r').read()
#
# cur.execute(db_create)

print("Table created successfully")

conn.commit()
conn.close()