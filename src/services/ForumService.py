from .DataBaseService import db_service

class ForumService:
    def get_forums_by_slug(self, data):
        cmd = '''SELECT * FROM forums f WHERE f.slug = '{slug}';
                        '''.format(**data)

        result = {}
        db_service.execute(cmd)
        db_res = db_service.get_one()
        print('____')
        print(db_res)
        for key in db_res.keys():
            if key in data.keys():
                result[key] = db_res[key]
        result['user'] = db_res['author']
        return result

    def create(self, data):
        cmd = """INSERT INTO forums (slug, title, author)
                        VALUES ('{slug}', '{title}', '{user}');
        """.format(**data)

        db_service.execute(cmd)
        print(data)
        return data

    def check_errors(self, data):
        cmd = """SELECT CASE WHEN
                    (SELECT slug FROM forums f WHERE f.slug = '{slug}'  LIMIT 1) 
                    IS NOT NULL THEN TRUE ELSE FALSE END AS "conflict",
                    CASE WHEN 
                    (SELECT nickname FROM users u WHERE u.nickname = '{user}' LIMIT 1)
                    IS NOT NULL THEN FALSE ELSE TRUE END AS "not_found";                                
                """.format(**data)

        db_service.execute(cmd)
        result = db_service.get_one()
        db_service.reconnect()
        return result

forum_service = ForumService()
