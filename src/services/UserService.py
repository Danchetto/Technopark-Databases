from .DataBaseService import db_service

class UserService:
    def get_user_id(self, nickname):
        cmd = '''SELECT id FROM users WHERE nickname = '{nickname}'
        '''.format(nickname=nickname)

        db_service.execute(cmd)
        return db_service.get_all()

    def get_users_by_email_or_nick(self, data):
        cmd = '''SELECT * FROM users WHERE nickname = '{nickname}' OR email = '{email}'
                '''.format(**data)

        db_service.execute(cmd)
        return db_service.get_all()

    def get_user(self, data):
        cmd = '''SELECT * FROM users WHERE nickname = '{nickname}'
                        '''.format(**data)

        db_service.execute(cmd)
        return db_service.get_one()

    def create(self, data):
        cmd = '''INSERT INTO users (nickname, about, email, fullname) 
                        VALUES ('{nickname}', '{about}', '{email}', '{fullname}');'''.format(**data)

        db_service.execute(cmd)
        return data

    def update(self, data):
        cmd = """UPDATE users SET about = '{about}', email = '{email}', fullname = '{fullname}'
                        WHERE nickname = '{nickname}';""".format(**data)

        db_service.execute(cmd)
        db_service.reconnect()

        return data


    def check_errors(self, data):
        check_cmd = """SELECT CASE WHEN 
                        ( SELECT nickname FROM users WHERE nickname <> '{nickname}' AND LOWER(email) = LOWER('{email}')) 
                        IS NOT NULL THEN TRUE ELSE FALSE END AS "conflict",
                        CASE WHEN 
                        (SELECT nickname FROM users WHERE nickname = '{nickname}') 
                        IS NOT NULL THEN FALSE ELSE TRUE END AS "not_found";
        """.format(**data)

        db_service.execute(check_cmd)
        result = db_service.get_one()
        db_service.reconnect()
        return result

user_service = UserService()