import tornado.web, tornado.escape
from src.services.UserService import user_service

class UserCreateHandler(tornado.web.RequestHandler):
    def post(self, nickname):
        self.set_header("Content-Type", "application/json")
        data = tornado.escape.json_decode(self.request.body)
        data.update({'nickname': nickname})

        errors = user_service.check_errors(data)
        if errors['not_found'] and not errors['conflict']:
            self.set_status(201)
            self.write(tornado.escape.json_encode(user_service.create(data)))
            return
        self.set_status(409)
        users = user_service.get_users_by_email_or_nick(data)
        self.write(tornado.escape.json_encode(users))
        return



class UserProfileHandler(tornado.web.RequestHandler):
    def get(self, nickname):
        data = {'nickname': nickname}
        self.set_header("Content-Type", "application/json")

        response = user_service.get_user(data['nickname'])
        status = 200 if response else 404
        self.set_status(status)
        self.write(tornado.escape.json_encode(response))

        return

    def post(self, nickname):
        self.set_header("Content-Type", "application/json")
        data = tornado.escape.json_decode(self.request.body)
        data.update({'nickname': nickname})

        errors = user_service.check_errors(data)

        if errors['conflict']:
            self.set_status(409)
            error_result = {'message': "Can't find user"}
            self.write(tornado.escape.json_encode(error_result))
            return
        if errors['not_found']:
            self.set_status(404)
            error_result = {'message': "Can't find user"}
            self.write(tornado.escape.json_encode(error_result))
            return

        if 'email' not in data.keys():
            email = user_service.get_user(nickname)['email']
            data.update({'email': email})

        self.set_status(200)
        self.write(tornado.escape.json_encode(user_service.update(data)))

        return
