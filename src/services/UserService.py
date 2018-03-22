from src.models.UserModel import UserModel
from src.services import *

class UserService:
    def user_create(self, data):
        print(data)
        new_user = UserModel()
        new_user.fill_info(data['nickname'], data['about'], data['email'], data['fullname'])
        conn = psycopg2.connect(database="technopark", user="postgres", password="12345", host="127.0.0.1", port="5432")
        cur = conn.cursor()

        try:
            insert_cmd = '''INSERT INTO "user" (nickname, about, email, fullname) 
                            VALUES ('{nickname}', '{about}', '{email}', '{fullname}');'''.format(
                nickname=data['nickname'], about=data['about'], email=data['email'], fullname=data['fullname'])

            cur.execute(insert_cmd)
            conn.commit()

        except:
            conn.close()
            conn = psycopg2.connect(database="technopark", user="postgres", password="12345", host="127.0.0.1",
                                    port="5432")
            cur = conn.cursor()
            select_cmd = '''SELECT * FROM "user" WHERE nickname = '{nickname}';
            '''.format(nickname=data['nickname'])
            cur.execute(select_cmd)
            conn.commit()
            print(cur.fetchall())
            conn.close()

        return new_user