from src.DataBase import db_service
from src.tools.datetime import time_to_str

class ThreadService:
    def get_thread_by_id(self, id):
        cmd = """SELECT * FROM threads WHERE id = {id}
                                """.format(id=id)

        db_service.execute(cmd)
        result = db_service.get_one()
        if 'created' in result.keys() and result['created'] is not None:
            result['created'] = time_to_str(result['created'])
        return result

    def get_thread_by_slug(self, slug):
        cmd = """SELECT * FROM threads WHERE slug = '{slug}'
                                """.format(slug=slug)

        db_service.execute(cmd)
        result = db_service.get_one()
        if 'created' in result.keys() and result['created'] is not None:
            result['created'] = time_to_str(result['created'])
        return result

    def get_thread_by_title(self, title):
        cmd = """SELECT * FROM threads WHERE title = '{title}'
                                """.format(title=title)

        db_service.execute(cmd)
        result = db_service.get_one()
        if 'created' in result.keys() and result['created'] is not None:
            result['created'] = time_to_str(result['created'])
        return result

    def create(self, data):
        cmd = """INSERT INTO threads (author, message, title, forum{is_created}{is_slug})
                                VALUES ('{author}', '{message}', '{title}', '{forum}'{created_data}{slug_data}) RETURNING id;
                """.format(**data,
                           is_created=', created' if 'created' in data.keys() else '',
                           created_data=", '" + data['created'] + "'" if 'created' in data.keys() else '',
                           is_slug=', slug' if 'slug' in data.keys() else '',
                           slug_data=", '" + data['slug'] + "'" if 'slug' in data.keys() else '')

        db_service.execute(cmd)
        return self.get_thread_by_id(db_service.get_one()['id'])

    def update(self, data):
        cmd = """UPDATE threads SET {message}{dot}{title} WHERE {slug_or_id} = '{slug_or_id_data}';""" \
            .format(message="message='" + data['message'] + "'" if 'message' in data.keys() else '',
                    dot=', ' if len(data) == 3 else '',
                    title=" title='" + data['title'] + "'" if 'title' in data.keys() else '',
                    slug_or_id='slug' if 'slug' in data.keys() else 'id',
                    slug_or_id_data=data['slug'] if 'slug' in data.keys() else data['id'])

        db_service.execute(cmd)
        db_service.reconnect()

        if 'id' in data.keys():
            return self.get_thread_by_id(data['id'])
        return self.get_thread_by_id(data['slug'])

    def get_info(self, data):
        cmd = '''SELECT * from threads WHERE {slug_or_id} = '{slug_or_id_data}'
        '''.format(slug_or_id='slug' if 'slug' in data.keys() else 'id',
                    slug_or_id_data=data['slug'] if 'slug' in data.keys() else data['id'])

        db_service.execute(cmd)

    def vote(self, data):
        cmd = '''INSERT INTO votes (username, voice, thread) VALUES ('{nickname}', {voice}, {thread});
                  UPDATE threads SET votes = votes {number} WHERE id = {thread};
        '''.format(**data, number='+ ' + data['vote'].__str__() if data['vote'] > 0 else ' ' + data['vote'].__str__())

        db_service.execute(cmd)
        return

    def check_errors(self, data):
        # db_service.reconnect()
        cmd = """SELECT CASE WHEN 
                        (SELECT nickname FROM users u WHERE u.nickname = '{author}' LIMIT 1)
                        IS NOT NULL THEN FALSE ELSE TRUE END AS "user_not_found";
                        """.format(**data)
        db_service.execute(cmd)

        return db_service.get_one()

    def check_by_slug(self, slug):
        # db_service.reconnect()
        cmd = """SELECT CASE WHEN
                    (SELECT slug FROM threads t WHERE t.slug = '{slug}'  LIMIT 1) 
                    IS NOT NULL THEN TRUE ELSE FALSE END AS "conflict";
                    """.format(slug=slug)
        db_service.execute(cmd)

        return db_service.get_one()

    def check_by_id(self, id):
        # db_service.reconnect()
        cmd = """SELECT CASE WHEN
                    (SELECT id FROM threads t WHERE t.id = '{id}'  LIMIT 1) 
                    IS NOT NULL THEN TRUE ELSE FALSE END AS "conflict";
                    """.format(id=id)
        db_service.execute(cmd)

        return db_service.get_one()

    def check_to_vote(self, data):
        cmd = """SELECT CASE WHEN
                            (SELECT username FROM votes v WHERE v.username = '{nickname}' AND v.thread = {thread} LIMIT 1) 
                            IS NOT NULL THEN TRUE ELSE FALSE END AS "found",
                            CASE WHEN
                            (SELECT username FROM votes v WHERE v.username = '{nickname}' AND v.thread = {thread} AND voice = {voice} LIMIT 1) 
                            IS NOT NULL THEN TRUE ELSE FALSE END AS "conflict";
                            """.format(**data)
        db_service.execute(cmd)

        return db_service.get_one()

thread_service = ThreadService()