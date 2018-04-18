from .DataBaseService import db_service
from ..services.UserService import user_service
from src.tools.datetime import normalize_time, time_to_str


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
        cmd = """INSERT INTO forums (slug, title, author)
                        VALUES ('{slug}', '{title}', '{username}') RETURNING *;
        """.format(**data, username=author)

        db_service.execute(cmd)
        result = db_service.get_one()
        result['user'] = result['author']
        result.pop('author', None)
        return result

    def get_forum_threads(self, data):
        cmd = """SELECT t.author, t.created, t.forum, t.id, t.message, t.slug, t.title, t.votes FROM forums f
                JOIN threads t ON t.forum = f.title
                WHERE f.slug = '{slug}'                                
        """.format(**data)

        if data['since']:
            cmd += ' AND t.created'
            cmd += ' <= ' if data['desc'] else ' >= '
            cmd += data['since']

        order = 'DESC' if data['desc'] else 'ASC'
        cmd += ' ORDER BY t.created ' + order + ' LIMIT ' + data['limit']

        db_service.execute(cmd)
        return db_service.get_all()

    def get_forum_users(self, data):
        cmd = """SELECT u.nickname  FROM users u
                JOIN threads t ON u.nickname = f.author
                JOIN posts p ON u.nickname = p.author
                WHERE t.forum = '{slug}' OR p.forum = '{slug}'                               
        """.format(**data)

        if data['since']:
            cmd += 'AND t.created'
            cmd += '<=' if data['desc'] else '>='
            cmd += data['since'] + ' '

        order = 'DESC' if data['desc'] else 'ASC'
        cmd += 'ORDER BY t.created ' + order + 'LIMIT' + data['limit']

        db_service.execute(cmd)
        return db_service.get_all()


    def check_errors(self, data):
        db_service.reconnect()
        cmd = """SELECT CASE WHEN
                    (SELECT slug FROM forums f WHERE f.slug = '{slug}'  LIMIT 1) 
                    IS NOT NULL THEN TRUE ELSE FALSE END AS "conflict",
                    CASE WHEN 
                    (SELECT nickname FROM users u WHERE LOWER(u.nickname) = LOWER('{user}') LIMIT 1)
                    IS NOT NULL THEN FALSE ELSE TRUE END AS "not_found";                                
                """.format(**data)

        db_service.execute(cmd)
        result = db_service.get_one()
        db_service.reconnect()
        return result

forum_service = ForumService()
