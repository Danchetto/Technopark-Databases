import tornado.web, tornado.escape
from datetime import datetime
from src.services.ThreadService import thread_service
from src.services.PostService import post_service
from src.DataBase import db_service

class PostCreateHandler(tornado.web.RequestHandler):
    def post(self, slug_or_id):
        self.set_header("Content-Type", "application/json")
        data = tornado.escape.json_decode(self.request.body)
        try:
            thread_id = int(slug_or_id)
        except:
            slug = slug_or_id
            thread_id = thread_service.get_thread_by_slug(slug)['id']

        created = (datetime.now())
        # if 'created' in data:
        #     data['created'] = normalize_time(data['created'])

        forum = thread_service.get_thread_by_id(thread_id)['forum']
        result = []
        for post in data:
            post.update({'thread': thread_id, 'forum': forum, 'created': created})

            if 'parent' not in post:
                post.update({'parent': 0})

            if post['parent'] > 0:
                parent_path = post_service.get_post_by_id(post['parent'])['path']
                parent_path.append(post['parent'])
                errors = post_service.check_errors(post)
            else:
                parent_path = []
                errors = {'parent_not_found': False}

            post.update({'path': parent_path})

            thread_found = thread_service.check_by_id(post['thread'])
            if not thread_found['conflict']:
                self.set_status(404)
                self.write(tornado.escape.json_encode({'message': 'not found'}))
                return
            elif errors['parent_not_found']:
                self.set_status(409)
                self.write(tornado.escape.json_encode({'message': 'not found'}))
                return

            result.append(post_service.create(post))

        db_service.commit()
        self.set_status(201)
        self.write(tornado.escape.json_encode(result))


class PostDetailsHandler(tornado.web.RequestHandler):
    def get(self, id):
        self.set_header("Content-Type", "application/json")

        return

    def post(self, id):
        self.set_header("Content-Type", "application/json")
        data = tornado.escape.json_decode(self.request.body)
        data.update({'id': id})
        errors = post_service.check_not_found(data)

        if errors['not_found']:
            self.set_status(404)
            self.write(tornado.escape.json_encode({'message': 'not found'}))
            return

        self.set_status(201)

        self.write(tornado.escape.json_encode(post_service.update(data)))
        return
