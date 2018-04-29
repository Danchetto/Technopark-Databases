from DataBase import db_service
from tools.datetime import time_to_str

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

    def create(self, data):
        cmd = """INSERT INTO threads (author, message, title, forum{is_created}{is_slug})
                                VALUES ('{author}', '{message}', '{title}', '{forum}'{created_data}{slug_data}) RETURNING id;
                """.format(**data,
                           is_created=', created' if 'created' in data.keys() else '',
                           created_data=", '" + data['created'] + "'" if 'created' in data.keys() else '',
                           is_slug=', slug' if 'slug' in data.keys() else '',
                           slug_data=", '" + data['slug'] + "'" if 'slug' in data.keys() else '')

        db_service.execute(cmd)
        result = self.get_thread_by_id(db_service.get_one()['id'])
        db_service.execute("""INSERT INTO forum_users (user_nickname, forum) SELECT '{author}', '{forum}' 
                                  WHERE NOT EXISTS (SELECT forum FROM forum_users WHERE LOWER(user_nickname) = LOWER('{author}') AND forum = '{forum}');
                              UPDATE forums SET threads = threads + 1 WHERE LOWER(slug) = LOWER('{forum}');""".format(**data))
        return result

    def update(self, data):
        cmd = """UPDATE threads SET {message}{dot}{title} WHERE {slug_or_id} = '{slug_or_id_data}';
              """.format(message="message='" + data['message'] + "'" if 'message' in data.keys() else '',
                    dot=', ' if 'message' in data.keys() and 'title' in data.keys() else '',
                    title=" title='" + data['title'] + "'" if 'title' in data.keys() else '',
                    slug_or_id='slug' if data['slug'] else 'id',
                    slug_or_id_data=data['slug'] if data['slug'] else data['id'])

        db_service.execute(cmd)

        if data['id'] is not False:
            return self.get_thread_by_id(data['id'])
        return self.get_thread_by_slug(data['slug'])

    def vote(self, data):
        cmd = '''INSERT INTO votes (username, voice, thread) VALUES ('{nickname}', {voice}, {thread});
                  UPDATE threads SET votes = votes {number} WHERE id = {thread};
        '''.format(**data, number='+ ' + data['vote'].__str__() if data['vote'] > 0 else ' ' + data['vote'].__str__())

        db_service.execute(cmd)
        return

    def update_vote(self, data):
        cmd = '''UPDATE votes SET voice = {voice} WHERE LOWER(username) = LOWER('{nickname}');
                          UPDATE threads SET votes = votes {number} WHERE id = {thread};
                '''.format(**data,
                           number='+ ' + data['vote'].__str__() if data['vote'] > 0 else ' ' + data['vote'].__str__())

        db_service.execute(cmd)
        return

    def check_errors(self, data):
        cmd = """SELECT CASE WHEN 
                        (SELECT nickname FROM users u WHERE LOWER(u.nickname) = LOWER('{author}') LIMIT 1)
                        IS NOT NULL THEN FALSE ELSE TRUE END AS "user_not_found";
                        """.format(**data)
        db_service.execute(cmd)

        return db_service.get_one()

    def check_errors_vote(self, data):
        cmd = """SELECT CASE WHEN 
                        (SELECT nickname FROM users u WHERE LOWER(u.nickname) = LOWER('{nickname}') LIMIT 1)
                        IS NOT NULL THEN FALSE ELSE TRUE END AS "user_not_found";
                        """.format(**data)
        db_service.execute(cmd)

        return db_service.get_one()

    def check_by_slug(self, slug):
        cmd = """SELECT CASE WHEN
                    (SELECT slug FROM threads t WHERE t.slug = '{slug}' LIMIT 1) 
                    IS NOT NULL THEN TRUE ELSE FALSE END AS "conflict";
                    """.format(slug=slug)
        db_service.execute(cmd)

        return db_service.get_one()

    def check_by_id(self, id):
        cmd = """SELECT CASE WHEN
                    (SELECT id FROM threads t WHERE t.id = '{id}' LIMIT 1) 
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

    def get_posts_flat(self, data):
        cmd = """SELECT * FROM posts p
                        WHERE p.thread = {thread}                                
                """.format(**data)

        if data['since']:
            cmd += ' AND p.id'
            cmd += ' < ' if data['desc'] else ' > '
            cmd += data['since'].__str__()

        order = 'DESC' if data['desc'] else 'ASC'
        cmd += ' ORDER BY p.created ' + order + ', id ' + order + ' LIMIT ' + data['limit']

        db_service.execute(cmd)
        result = db_service.get_all()
        for post in result:
            post['created'] = time_to_str(post['created'])

        return result

    def get_posts_tree(self, data):
        cmd = """SELECT * FROM posts p
                        WHERE p.thread = {thread}                                
                """.format(**data)

        if data['since']:
            cmd += ' AND p.path'
            cmd += ' < ' if data['desc'] else ' > '
            cmd += '(SELECT path FROM posts WHERE id = ' + data['since'].__str__() + ')'

        order = 'DESC' if data['desc'] else 'ASC'
        cmd += ' ORDER BY p.path ' + order + ' LIMIT ' + data['limit']

        db_service.execute(cmd)
        result = db_service.get_all()
        for post in result:
            post['created'] = time_to_str(post['created'])
        return result

    def get_posts_parent_tree(self, data):
        root_posts = self.get_root_posts(data)

        result = []
        data.update({'parent': 0})
        for parent in root_posts:
            data['parent'] = parent['id']

            cmd = """SELECT * FROM posts p
                                    WHERE p.thread = {thread} and p.path[1] = {parent}                           
                            """.format(**data)

            if data['since']:
                cmd += ' AND p.path[1]'
                cmd += ' < ' if data['desc'] else ' > '
                cmd += '(SELECT path[1] FROM posts WHERE id = ' + data['since'].__str__() + ')'

            # order = 'DESC' if data['desc'] else 'ASC'
            cmd += ' ORDER BY p.path, p.id'

            db_service.execute(cmd)
            current_result = db_service.get_all()
            for post in current_result:
                post['created'] = time_to_str(post['created'])
            result.extend(current_result)

        return result

    def get_root_posts(self, data):
        cmd = """SELECT id FROM posts p
                                WHERE p.thread = {thread} AND p.parent = 0                             
                        """.format(**data)

        if data['since']:
            cmd += ' AND p.path[1]'
            cmd += ' < ' if data['desc'] else ' > '
            cmd += '(SELECT path[1] FROM posts WHERE id = ' + data['since'].__str__() + ')'

        order = 'DESC' if data['desc'] else 'ASC'
        cmd += ' ORDER BY p.id ' + order + ' LIMIT ' + data['limit']

        db_service.execute(cmd)
        result = db_service.get_all()

        return result


thread_service = ThreadService()
