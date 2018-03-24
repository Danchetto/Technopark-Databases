import tornado.web, tornado.escape
from src.services.ForumService import forum_service

class ForumCreateHandler(tornado.web.RequestHandler):
    def post(self):
        self.set_header("Content-Type", "application/json")
        data = tornado.escape.json_decode(self.request.body)

        errors = forum_service.check_errors(data)
        print(errors)
        if errors['conflict']:
            self.set_status(409)
            forum = forum_service.get_forums_by_slug(data)
            print(forum)
            self.write(tornado.escape.json_encode(forum))
            return
        elif errors['not_found']:
            self.set_status(404)
            self.write(tornado.escape.json_encode({'message': 'user not found'}))
            return


        self.set_status(201)
        self.write(tornado.escape.json_encode(forum_service.create(data)))
