import tornado.web, tornado.escape
from src.services.ThreadService import thread_service
from src.services.ForumService import forum_service
from src.tools.datetime import normalize_time

class ThreadCreateHandler(tornado.web.RequestHandler):
    def post(self, slug):
        self.set_header("Content-Type", "application/json")
        data = tornado.escape.json_decode(self.request.body)
        # if 'created' in data:
        #     data['created'] = normalize_time(data['created'])

        forum = forum_service.get_forum_by_slug(slug)['slug']
        data.update({'forum': forum})

        errors = thread_service.check_errors(data)
        if errors['user_not_found'] or errors['forum_not_found']:
            self.set_status(404)
            self.write(tornado.escape.json_encode({'message': 'not found'}))
            return
        elif errors['conflict']:
            self.set_status(409)
            self.write(tornado.escape.json_encode(thread_service.get_thread_by_slug(data)))
            return

        self.set_status(201)
        self.write(tornado.escape.json_encode(thread_service.create(data)))

class ThreadDetailsHandler(tornado.web.RequestHandler):
    def get(self, slug_or_id):
        self.set_header("Content-Type", "application/json")
        try:
            thread_id = int(slug_or_id)
            errors = thread_service.check_by_id({'id': thread_id})
            if not errors['conflict']:
                self.set_status(404)
                self.write(tornado.escape.json_encode({'message': 'forum not found'}))
                return
            self.set_status(200)
            self.write(tornado.escape.json_encode(thread_service.get_thread_by_id(thread_id)))

        except:
            slug = slug_or_id
            errors = thread_service.check_by_slug({'slug': slug})
            if not errors['conflict']:
                self.set_status(404)
                self.write(tornado.escape.json_encode({'message': 'forum not found'}))
                return
            self.set_status(200)
            self.write(tornado.escape.json_encode(thread_service.get_thread_by_slug(slug)))

    def post(self, slug_or_id):
        self.set_header("Content-Type", "application/json")
        data = tornado.escape.json_decode(self.request.body)

        try:
            thread_id = int(slug_or_id)
            data.update({'id': thread_id})
            errors = thread_service.check_by_id(data)
        except:
            slug = slug_or_id
            data.update({'slug': slug})
            errors = thread_service.check_by_slug(data)

        if not errors['conflict']:
            self.set_status(404)
            self.write(tornado.escape.json_encode({'message': 'forum not found'}))
            return

        self.set_status(200)
        self.write(tornado.escape.json_encode(thread_service.update(data)))
