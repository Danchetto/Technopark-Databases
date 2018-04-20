import tornado.web, tornado.escape
from src.services.ThreadService import thread_service
from src.services.ForumService import forum_service

class ThreadCreateHandler(tornado.web.RequestHandler):
    def post(self, slug):
        self.set_header("Content-Type", "application/json")
        data = tornado.escape.json_decode(self.request.body)

        if 'slug' in data.keys():
            conflict_check = thread_service.check_by_slug(data['slug'])
        else:
            conflict_check = {'conflict': False}

        errors = thread_service.check_errors(data)
        if errors['user_not_found'] or not forum_service.check_errors({'slug': slug, 'user': ''})['conflict']:
            self.set_status(404)
            self.write(tornado.escape.json_encode({'message': 'not found'}))
            return
        elif conflict_check['conflict']:
            self.set_status(409)
            self.write(tornado.escape.json_encode(thread_service.get_thread_by_slug(data['slug'])))
            return

        forum = forum_service.get_forum_by_slug(slug)['slug']
        data.update({'forum': forum})

        self.set_status(201)
        self.write(tornado.escape.json_encode(thread_service.create(data)))

class ThreadDetailsHandler(tornado.web.RequestHandler):
    def get(self, slug_or_id):
        self.set_header("Content-Type", "application/json")
        try:
            thread_id = int(slug_or_id)
            errors = thread_service.check_by_id(thread_id)
            if not errors['conflict']:
                self.set_status(404)
                self.write(tornado.escape.json_encode({'message': 'forum not found'}))
                return
            self.set_status(200)
            self.write(tornado.escape.json_encode(thread_service.get_thread_by_id(thread_id)))

        except:
            slug = slug_or_id
            errors = thread_service.check_by_slug(slug)
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
            errors = thread_service.check_by_id(thread_id)
        except:
            slug = slug_or_id
            data.update({'slug': slug})
            errors = thread_service.check_by_slug(slug)

        if not errors['conflict']:
            self.set_status(404)
            self.write(tornado.escape.json_encode({'message': 'forum not found'}))
            return

        self.set_status(200)
        self.write(tornado.escape.json_encode(thread_service.update(data)))


class ThreadVoteHandler(tornado.web.RequestHandler):
    def post(self, slug_or_id):
        self.set_header("Content-Type", "application/json")
        data = tornado.escape.json_decode(self.request.body)
        try:
            thread_id = int(slug_or_id)
            thread_found = thread_service.check_by_id(thread_id)

        except:
            slug = slug_or_id
            thread_found = thread_service.check_by_slug(slug)
            thread_id = thread_service.get_thread_by_slug(slug)['id']

        if not thread_found['conflict']:
            self.set_status(404)
            self.write(tornado.escape.json_encode({'message': 'not found'}))
            return

        data.update({'thread': thread_id})
        self.set_status(200)
        data.update({'vote': data['voice']})
        errors = thread_service.check_to_vote(data)
        if errors['found'] and not errors['conflict']:
            data['vote'] = -2 if data['vote'] == -1 else 2
        if errors['conflict']:
            thread = thread_service.get_thread_by_id(thread_id)
            self.write(tornado.escape.json_encode(thread))
            return
        thread_service.vote(data)
        thread = thread_service.get_thread_by_id(thread_id)
        self.write(tornado.escape.json_encode(thread))
        return
