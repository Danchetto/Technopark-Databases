from .DataBaseService import db_service
from src.tools.datetime import normalize_time, time_to_str

class ThreadService:
    def get_forum_title(self, data):
        cmd = """SELECT f.title FROM forums f
                        JOIN threads t ON (f.slug = t.slug) WHERE t.slug = '{slug}';
                        """.format(**data)

        db_service.execute(cmd)
        result = db_service.get_one()
        print(result)
        return result

    def get_thread_by_slug(self, data):
        cmd = """SELECT * FROM threads WHERE slug = '{slug}'
                                """.format(**data)

        db_service.execute(cmd)
        result = db_service.get_one()
        result['created'] = time_to_str(result['created']) + 'Z'
        return result

    def create(self, data):
        cmd = """INSERT INTO threads (author, created, message, title, forum, slug, votes)
                                VALUES ('{author}', '{created}', '{message}', '{title}', '{forum}', '{slug}', 0) RETURNING id;
                """.format(**data)

        db_service.execute(cmd)
        data.update(db_service.get_one())
        return data

    def check_errors(self, data):
        cmd = """SELECT CASE WHEN
                        (SELECT slug FROM threads t WHERE t.title = '{title}' AND t.slug = '{slug}'  LIMIT 1) 
                        IS NOT NULL THEN TRUE ELSE FALSE END AS "conflict",
                        CASE WHEN 
                        (SELECT nickname FROM users u WHERE u.nickname = '{author}' LIMIT 1)
                        IS NOT NULL THEN FALSE ELSE TRUE END AS "user_not_found",
                        CASE WHEN 
                        (SELECT slug FROM forums f WHERE f.slug = '{slug}' LIMIT 1)
                        IS NOT NULL THEN FALSE ELSE TRUE END AS "forum_not_found";
                        """.format(**data)
        db_service.execute(cmd)

        return db_service.get_one()

thread_service = ThreadService()