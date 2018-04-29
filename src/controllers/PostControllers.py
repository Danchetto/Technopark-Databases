import tornado.web, tornado.escape
import json
from services.ThreadService import thread_service
from services.PostService import post_service
from DataBase import db_service
from tools.datetime import get_time, DateTimeEncoder
# import arrow

class PostCreateHandler(tornado.web.RequestHandler):
    def post(self, slug_or_id):
        created = get_time()
        self.set_header("Content-Type", "application/json")
        data = tornado.escape.json_decode(self.request.body)
        try:
            thread_id = int(slug_or_id)
        except:
            slug = slug_or_id
            if not thread_service.check_by_slug(slug)['conflict']:
                self.set_status(404)
                self.write(tornado.escape.json_encode({'message': 'not found'}))
                return
            thread_id = thread_service.get_thread_by_slug(slug)['id']

        if not thread_service.check_by_id(thread_id)['conflict']:
            self.set_status(404)
            self.write(tornado.escape.json_encode({'message': 'not found'}))
            return

        forum = thread_service.get_thread_by_id(thread_id)['forum']
        result = []
        for post in data:
            post.update({'thread': thread_id, 'forum': forum, 'created': created})

            if 'parent' not in post:
                post.update({'parent': 0})

            if post_service.check_user(post)['user_not_found']:
                self.set_status(404)
                self.write(tornado.escape.json_encode({'message': 'not found'}))
                return

            if post['parent'] > 0:
                if post_service.check_parent(post)['parent_conflict']:
                    self.set_status(409)
                    self.write(tornado.escape.json_encode({'message': 'not found'}))
                    return

                parent_path = post_service.get_post_by_id(post['parent'])['path']
                parent_path.append(post['parent'])
            else:
                parent_path = []
                errors = {'parent_conflict': False}

            id = post_service.get_next_id()
            post.update({'path': parent_path, 'id': id})

            thread_found = thread_service.check_by_id(post['thread'])
            if not thread_found['conflict']:
                self.set_status(404)
                self.write(tornado.escape.json_encode({'message': 'not found'}))
                return

            current_result = post_service.create(post)
            result.append(current_result)

        db_service.commit()
        self.set_status(201)
        self.write(json.dumps(result, cls=DateTimeEncoder))
        return


class PostDetailsHandler(tornado.web.RequestHandler):
    def get(self, id):
        self.set_header("Content-Type", "application/json")

        try:
            related = (self.get_argument('related').split(','))
        except:
            related = []
        errors = post_service.check_not_found({'id': id})

        if errors['not_found']:
            self.set_status(404)
            self.write(tornado.escape.json_encode({'message': 'not found'}))
            return
        self.set_status(200)
        data = {'id': id, 'related': related}
        self.write(json.dumps((post_service.details(data)), cls=DateTimeEncoder))
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
        post = post_service.get_post_by_id(data['id'])
        self.set_status(200)
        if len(data.keys()) == 1 or data['message'] == post['message']:
            self.write(json.dumps((post), cls=DateTimeEncoder))
        else:
            self.write(json.dumps((post_service.update(data)), cls=DateTimeEncoder))
