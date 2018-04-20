import tornado.web, tornado.escape
from datetime import datetime
from src.services.ThreadService import thread_service
from src.services.PostService import post_service

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

        for post in data:
            post.update({'thread': thread_id, 'forum': forum, 'created': created})

            if 'parent' not in post:
                post.update({'parent': 0})
            errors = post_service.check_errors(post) if post['parent'] > 0 else {'parent_not_found': False}
            thread_found = thread_service.check_by_id(post['thread'])
            if not thread_found['conflict']:
                self.set_status(404)
                self.write(tornado.escape.json_encode({'message': 'not found'}))
                return
            elif errors['parent_not_found']:
                self.set_status(409)
                self.write(tornado.escape.json_encode({'message': 'not found'}))
                return

        post_service.create(data)
        self.set_status(201)
        self.write(tornado.escape.json_encode(post_service.create(data)))