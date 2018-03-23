from .DataBaseService import db_service

class ForumService:
    def forum_create(self, data):
        try:
            insert_cmd = """INSERT INTO forum (slug, title, userid)
                            SELECT id FROM "user" u WHERE u.nickname = {nickname} AS user_id 
                            VALUES ('{slug}', '{title}', user_id)
            """.format(slug=data['slug'], title=data['title'], nickname=data['nickname'])

            db_service.execute(insert_cmd)

        except:
            print(1)
