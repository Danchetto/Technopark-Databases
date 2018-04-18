import tornado.web, tornado.escape
from datetime import datetime
from src.services.ThreadService import thread_service
from src.services.PostService import post_service
from src.services.ForumService import forum_service
from src.tools.datetime import normalize_time

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

            errors = post_service.check_errors(post)
            if errors['thread_not_found']:
                self.set_status(404)
                self.write(tornado.escape.json_encode({'message': 'not found'}))
                return
            elif errors['parent_not_found']:
                self.set_status(409)
                self.write(tornado.escape.json_encode({'message': 'not found'}))
                return

        post_service.create(data)
        self.set_status(201)
        self.write(tornado.escape.json_encode(thread_service.create(data)))