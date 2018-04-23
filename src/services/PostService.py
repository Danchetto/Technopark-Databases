from src.DataBase import db_service
from src.tools.datetime import time_to_str

class PostService:
    def get_post_path(self, id):
        cmd = """SELECT path FROM posts WHERE id = {id}""".format(id=id)

        db_service.execute(cmd)
        return db_service.get_one()

    def get_post_by_id(self, id):
        cmd = """SELECT * FROM posts WHERE id = {id}""".format(id=id)

        db_service.execute(cmd)
        return db_service.get_one()

    def create(self, post):
        cmd = """INSERT INTO posts (author, message, forum, thread, created, parent, path)
                                        VALUES ('{author}', '{message}', '{forum}', '{thread}', '{created}', '{parent}', '{path_data}') RETURNING *;
                        """.format(**post, path_data='{' + ', '.join('{0}'.format(n) for n in post['path']) + '}')

        db_service.execute_only(cmd)
        result = db_service.get_one()
        if 'created' in result.keys() and result['created'] is not None:
            result['created'] = time_to_str(result['created'])
        return result

    def update(self, data):
        cmd = """UPDATE posts SET {message} isEdited = TRUE WHERE id = {id};"""\
            .format(message="message='" + data['message'] + "'," if 'message' in data.keys() else '',
                    id=id)

        db_service.execute(cmd)
        return self.get_post_by_id(data['id'])

    def check_errors(self, data):
        cmd = '''SELECT CASE WHEN
                    (SELECT id FROM posts p WHERE p.id = {parent} LIMIT 1) 
                    IS NULL THEN TRUE ELSE FALSE END AS "parent_not_found";
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