from DataBase import db_service
from services.UserService import user_service
from tools.datetime import normalize_time, time_to_str


class ForumService:
    def get_forum_by_slug(self, slug):
        cmd = '''SELECT * FROM forums f WHERE f.slug = '{slug}';
                        '''.format(slug=slug)

        db_service.execute(cmd)
        db_res = db_service.get_one()
        db_res['user'] = db_res['author']
        db_res.pop('author', None)

        return db_res

    def get_forum_by_id(self, id):
        cmd = '''SELECT * FROM forums f WHERE f.id = '{id}';
                        '''.format(id=id)

        db_service.execute(cmd)
        db_res = db_service.get_one()
        db_res['user'] = db_res['author']
        db_res.pop('author', None)

        return db_res

    def create(self, data):
        author = user_service.get_user(data['user'])['nickname']
        db_service.reconnect()
        cmd = """INSERT INTO forums (slug, title, author, posts, threads)
                        VALUES ('{slug}', '{title}', '{username}', 0, 0) RETURNING *;
        """.format(**data, username=author)

        db_service.execute(cmd)
        result = db_service.get_one()
        result['user'] = result['author']
        result.pop('author', None)
        return result

    def get_forum_threads(self, data):
        cmd = """SELECT * FROM threads t
                WHERE LOWER(t.forum) = LOWER('{slug}')                                
        """.format(**data)

        if data['since']:
            cmd += ' AND t.created'
            cmd += ' <= ' if data['desc'] else ' >= '
            cmd += "'" + data['since'] + "'"

        order = 'DESC' if data['desc'] else 'ASC'
        cmd += ' ORDER BY t.created ' + order
        cmd += ' LIMIT ' + data['limit'] if data['limit'] else ''

        db_service.execute(cmd)
        result = db_service.get_all()
        for thread in result:
            thread['created'] = time_to_str(thread['created'])

        return result

    def get_forum_users(self, data):
        cmd = """SELECT u.* FROM users u
                JOIN forum_users fu ON LOWER(u.nickname) = LOWER(fu.user_nickname)
                WHERE LOWER(fu.forum) = LOWER('{slug}')                               
        """.format(**data)

        if data['since']:
            cmd += 'AND LOWER(u.nickname)'
            cmd += '<' if data['desc'] else '>'
            cmd += "LOWER('" + data['since'] + "')"

        order = 'DESC' if data['desc'] else 'ASC'
        cmd += ' ORDER BY LOWER(u.nickname) ' + order
        cmd += ' LIMIT ' + data['limit'] if data['limit'] else ''

        db_service.execute(cmd)
        result = db_service.get_all()

        return result

    def check_errors(self, data):
        cmd = """SELECT CASE WHEN
                    (SELECT slug FROM forums f WHERE f.slug = '{slug}' LIMIT 1) 
                    IS NOT NULL THEN TRUE ELSE FALSE END AS "conflict",
                    CASE WHEN 
                    (SELECT nickname FROM users u WHERE LOWER(u.nickname) = LOWER('{user}') LIMIT 1)
                    IS NOT NULL THEN FALSE ELSE TRUE END AS "not_found";                                
                """.format(**data)

        db_service.execute(cmd)
        result = db_service.get_one()
        return result

forum_service = ForumService()
