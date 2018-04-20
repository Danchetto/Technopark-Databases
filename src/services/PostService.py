from src.DataBase import db_service
from src.tools.datetime import time_to_str

class PostService:
    def create(self, data):
        result = []
        for post in data:
            cmd = """INSERT INTO posts (author, message, forum, thread, created)
                                            VALUES ('{author}', '{message}', '{forum}', '{thread}', '{created}') RETURNING *;
                            """.format(**post)

            db_service.execute(cmd)
            current = db_service.get_one()
            if 'created' in current.keys() and current['created'] is not None:
                current['created'] = time_to_str(current['created'])
            result.append(current)

        return result

    def check_errors(self, data):
        cmd = '''SELECT CASE WHEN
                    (SELECT id FROM posts p WHERE p.id = {parent} LIMIT 1) 
                    IS NOT NULL THEN TRUE ELSE FALSE END AS "parent_not_found";
        '''.format(**data)
        db_service.execute(cmd)
        return db_service.get_one()

post_service = PostService()