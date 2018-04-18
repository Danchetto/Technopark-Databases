from .DataBaseService import db_service

class PostService:
    def create(self, data):
        for post in data:
            cmd = """INSERT INTO posts (author, message, forum, thread, created)
                                            VALUES ('{author}', '{message}', '{forum}', '{thread}', '{created}') RETURNING id;
                            """.format(**data)

            db_service.execute(cmd)

post_service = PostService()