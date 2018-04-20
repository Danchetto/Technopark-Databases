from src.DataBase import db_service

class UserService:
    def get_users_by_email_or_nick(self, data):
        cmd = '''SELECT * FROM users WHERE LOWER(nickname) = LOWER('{nickname}') OR email = '{email}'
                '''.format(**data)

        db_service.execute(cmd)
        return db_service.get_all()

    def get_user(self, username):
        cmd = '''SELECT * FROM users WHERE LOWER(nickname) = LOWER('{nickname}')
                        '''.format(nickname=username)

        db_service.execute(cmd)
        return db_service.get_one()

    def create(self, data):
        cmd = '''INSERT INTO users (nickname, about, email, fullname) 
                        VALUES ('{nickname}', '{about}', '{email}', '{fullname}');'''.format(**data)

        db_service.execute(cmd)
        return data

    def update(self, data):
        cmd = """UPDATE users SET {about}{email}{fullname} WHERE LOWER(nickname) = LOWER('{nickname}');"""\
            .format(about="about='" + data['about'] + "'," if 'about' in data.keys() else '',
                    email=" email='" + data['email'] + "'" if 'email' in data.keys() else '',
                    fullname=", fullname='" + data['fullname'] + "'" if 'fullname' in data.keys() else '',
                    nickname=data['nickname'])

        db_service.execute(cmd)
        db_service.reconnect()

        return self.get_user(data['nickname'])


    def check_errors(self, data):
        result = {}
        if 'email' in data.keys():
            check_cmd = """SELECT CASE WHEN 
                            ( SELECT nickname FROM users WHERE LOWER(nickname) <> LOWER('{nickname}') AND LOWER(email) = LOWER('{email}'))
                            IS NOT NULL THEN TRUE ELSE FALSE END AS "conflict",
                            CASE WHEN 
                            (SELECT nickname FROM users WHERE LOWER(nickname) = LOWER('{nickname}')) 
                            IS NOT NULL THEN FALSE ELSE TRUE END AS "not_found";
            """.format(**data)
        else:
            check_cmd = """SELECT CASE WHEN
                            (SELECT nickname FROM users WHERE LOWER(nickname) = LOWER('{nickname}')) 
                            IS NOT NULL THEN FALSE ELSE TRUE END AS "not_found";
                        """.format(**data)
            result.update({'conflict': False})

        db_service.execute(check_cmd)
        result.update(db_service.get_one())
        db_service.reconnect()
        return result

user_service = UserService()