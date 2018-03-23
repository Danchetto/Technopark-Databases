from src.models.UserModel import UserModel
from .DataBaseService import db_service
import psycopg2

class UserService:
    def get_user_id(self, nickname):
        cmd = '''SELECT id FROM "user" WHERE nickname = '{nickname}'
        '''.format(nickname=nickname)

        db_service.execute(cmd)
        return db_service.get_result()[0]

    def create(self, data):
        try:
            insert_cmd = '''INSERT INTO "user" (nickname, about, email, fullname) 
                            VALUES ('{nickname}', '{about}', '{email}', '{fullname}');'''.format(**data)

            db_service.execute(insert_cmd)
            result = data
            status = 201

        except psycopg2.IntegrityError:
            db_service.reconnect()
            select_cmd = '''SELECT * FROM "user" WHERE nickname = '{nickname}' OR email = '{email}';
            '''.format(**data)
            db_service.execute(select_cmd)
            result = db_service.get_result()
            status = 409

        return (status, result)

    def update(self, data):
        insert_cmd = """UPDATE "user" SET about = '{about}', email = '{email}', fullname = '{fullname}'
                        WHERE nickname = '{nickname}';""".format(**data)

        db_service.execute(insert_cmd)
        db_service.reconnect()

        return data

    def get(self, data):
        try:
            insert_cmd = """SELECT about, email, fullname FROM "user"
                            WHERE nickname = '{nickname}';""".format(
                nickname=data['nickname'])

            db_service.execute(insert_cmd)
            arr = db_service.get_result()[0]
            result = {'about': arr[0], 'email': arr[1], 'fullname': arr[2], 'nickname': data['nickname']}
            status = 200

        except:
            status = 409
            db_service.reconnect()
            select_cmd = '''SELECT id FROM "user" WHERE nickname = '{nickname}';
                                '''.format(**data)
            db_service.execute(select_cmd)
            result = {'message': "Can't find user with id #{id}\n".format(id=db_service.get_result()[0])}

        return (status, result)

    def check_errors(self, data):
        check_cmd = """SELECT CASE WHEN 
                        ( SELECT nickname FROM "user" WHERE nickname <> '{nickname}' AND LOWER(email) <> LOWER('{email}') LIMIT 1) 
                        IS NOT NULL THEN TRUE ELSE FALSE END AS "conflict",
                        CASE WHEN 
                        (SELECT nickname FROM "user" WHERE nickname = '{nickname}' LIMIT 1) 
                        IS NOT NULL THEN FALSE ELSE TRUE END AS "notfound";
        """.format(**data)

        db_service.execute(check_cmd)
        return db_service.get_result()[0]

user_service = UserService()