import tornado.web, tornado.escape
from src.services.ThreadService import thread_service
from src.tools.datetime import normalize_time

class ThreadCreateHandler(tornado.web.RequestHandler):
    def post(self, slug):
        self.set_header("Content-Type", "application/json")
        data = tornado.escape.json_decode(self.request.body)
        # if 'created' in data:
        #     data['created'] = normalize_time(data['created'])

        data.update({'slug': slug})
        forum = thread_service.get_forum_title(data)
        data.update({'forum': forum})

        errors = thread_service.check_errors(data)
        print(errors)
        if errors['user_not_found'] or errors['forum_not_found']:
            self.set_status(404)
            self.write(tornado.escape.json_encode({'message': 'not found'}))
            return
        elif errors['conflict']:
            self.set_status(409)
            print(1)
            self.write(tornado.escape.json_encode(thread_service.get_thread_by_slug(data)))
            return

        self.set_status(201)
        self.write(tornado.escape.json_encode(thread_service.create(data)))