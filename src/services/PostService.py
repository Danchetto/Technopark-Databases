from src.DataBase import db_service
from src.tools.datetime import time_to_str

class PostService:
    def get_next_id(self):
        cmd = "SELECT nextval(pg_get_serial_sequence('posts', 'id'))"
        db_service.execute(cmd)
        return db_service.get_one()['nextval']

    def get_post_path(self, id):
        cmd = """SELECT path FROM posts WHERE id = {id}""".format(id=id)

        db_service.execute(cmd)
        return db_service.get_one()

    def get_post_by_id(self, id):
        cmd = """SELECT * FROM posts WHERE id = {id}""".format(id=id)

        db_service.execute(cmd)
        result = db_service.get_one()
        if 'created' in result.keys() and result['created'] is not None:
            result['created'] = time_to_str(result['created'])
        result['isEdited'] = result['isedited']
        result.pop('isedited')

        return result

    def details(self, data):
        db_service.reconnect()
        cmd = """SELECT * FROM posts p WHERE p.id = {id};
        """.format(**data)
        db_service.execute(cmd)
        result = {"post": db_service.get_one()}
        if 'created' in result['post'].keys() and result['post']['created'] is not None:
            result['post']['created'] = time_to_str(result['post']['created'])
            result['post']['isEdited'] = result['post']['isedited']

        if 'author' in data['related']:
            cmd += """SELECT u.email, u.about, u.nickname, u.fullname
                      FROM users u JOIN posts p ON p.author = u.nickname WHERE p.id = {id}';
                    """.format(**data)
            db_service.execute(cmd)
            result.update({"author": db_service.get_one()})

        if 'thread' in data['related']:
            cmd += """SELECT t.author, t.created, t.forum, t.id, t.message, t.slug, t.title, t.votes
                      FROM threads t JOIN posts p ON p.thread = t.id WHERE p.id = {id}';
                    """.format(**data)
            db_service.execute(cmd)
            result.update({"thread": db_service.get_one()})
            if 'created' in result['thread'].keys() and result['thread']['created'] is not None:
                result['thread']['created'] = time_to_str(result['thread']['created'])

        if 'forum' in data['related']:
            cmd += """SELECT f.slug, f.posts, f.threads, f.title, f.user
                      FROM forum f JOIN posts p ON p.forum = f.slug WHERE p.id = {id}' ;
                    """.format(**data)
            db_service.execute(cmd)
            result.update({"forum": db_service.get_one()})
            if 'created' in result['forum'].keys() and result['forum']['created'] is not None:
                result['forum']['created'] = time_to_str(result['forum']['created'])

        return result

    def create(self, post):
        cmd = """INSERT INTO posts (id, author, message, forum, thread, created, parent, path)
                                        VALUES ({id}, '{author}', '{message}', '{forum}', '{thread}', 
                                        '{created}', '{parent}', array_append(ARRAY[{path_data}]::integer[], {id})) RETURNING *;
                        """.format(**post, path_data=', '.join('{0}'.format(n) for n in post['path']))

        db_service.execute_only(cmd)
        result = db_service.get_one()
        if 'created' in result.keys() and result['created'] is not None:
            result['created'] = time_to_str(result['created'])

        db_service.execute("""INSERT INTO forum_users (user_nickname, forum) SELECT '{author}', '{forum}' 
                                  WHERE NOT EXISTS (SELECT forum FROM forum_users WHERE LOWER(user_nickname) = LOWER('{author}') AND forum = '{forum}');
                            UPDATE forums SET posts = posts + 1 WHERE LOWER(slug) = LOWER('{forum}');""".format(**post))

        return result

    def update(self, data):
        cmd = """UPDATE posts SET {message_data} isEdited = TRUE WHERE id = {id};
""".format(message_data="message='" + data['message'] + "'," if 'message' in data.keys() else '', **data)

        db_service.execute(cmd)
        return self.get_post_by_id(data['id'])

    def check_parent(self, data):
        cmd = '''SELECT CASE WHEN
                    (SELECT id FROM posts p WHERE p.id = {parent} AND p.thread = {thread} LIMIT 1) 
                    IS NULL THEN TRUE ELSE FALSE END AS "parent_conflict";
                     
        '''.format(**data)
        db_service.execute(cmd)
        return db_service.get_one()

    def check_user(self, data):
        cmd = '''SELECT CASE WHEN
                            (SELECT nickname FROM users WHERE LOWER(nickname) = LOWER('{author}') LIMIT 1) 
                            IS NULL THEN TRUE ELSE FALSE END AS "user_not_found";
                '''.format(**data)
        db_service.execute(cmd)
        return db_service.get_one()

    def check_not_found(self, data):
        cmd = '''SELECT CASE WHEN
                            (SELECT id FROM posts p WHERE p.id = {id} LIMIT 1) 
                            IS NULL THEN TRUE ELSE FALSE END AS "not_found";
                '''.format(**data)
        db_service.execute(cmd)
        return db_service.get_one()

post_service = PostService()