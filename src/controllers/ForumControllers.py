import tornado.web, tornado.escape
from src.services.ForumService import forum_service

class ForumCreateHandler(tornado.web.RequestHandler):
    def post(self):
        self.set_header("Content-Type", "application/json")
        data = tornado.escape.json_decode(self.request.body)
        errors = forum_service.check_errors(data)

        if errors['conflict']:
            self.set_status(409)
            forum = forum_service.get_forum_by_slug(data['slug'])
            print(forum)
            self.write(tornado.escape.json_encode(forum))
            return
        elif errors['not_found']:
            self.set_status(404)
            self.write(tornado.escape.json_encode({'message': 'user not found'}))
            return


        self.set_status(201)
        self.write(tornado.escape.json_encode(forum_service.create(data)))

class ForumDetailsHandler(tornado.web.RequestHandler):
    def get(self, slug):
        self.set_header("Content-Type", "application/json")
        data = {'slug': slug, 'user': '', 'title': ''}
        errors = forum_service.check_errors(data)

        if errors['conflict']:
            self.set_status(200)
            forum = forum_service.get_forum_by_slug(data['slug'])
            print(forum)
            self.write(tornado.escape.json_encode(forum))
            return
        self.set_status(404)
        self.write(tornado.escape.json_encode({'message': 'forum not found'}))

class ForumThreadsHandler(tornado.web.RequestHandler):
    def get(self, slug):
        self.set_header("Content-Type", "application/json")
        # data = tornado.escape.json_decode(self.request.body)
        try:
            limit = self.get_argument('limit')
        except:
            limit = None

        try:
            since = self.get_argument('since')
        except:
            since = None

        try:
            desc = bool(self.get_argument('desc'))
        except:
            desc = None

        data = {'slug': slug, 'limit': limit, 'since': since, 'desc': desc, 'user': ''}
        errors = forum_service.check_errors(data)

        if errors['conflict']:
            self.set_status(200)
            threads = forum_service.get_forum_threads(data)
            print(threads)
            self.write(tornado.escape.json_encode(threads))
            return
        self.set_status(404)
        self.write(tornado.escape.json_encode({'message': 'forum not found'}))
