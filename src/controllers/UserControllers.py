import tornado.web, tornado.escape
from src.services.UserService import user_service

class UserCreateHandler(tornado.web.RequestHandler):
    def post(self, nickname):
        self.set_header("Content-Type", "application/json")
        data = tornado.escape.json_decode(self.request.body)
        data.update({'nickname': nickname})

        response = user_service.create(data)
        if response[0] != True:
            self.set_status(201)
        else:
            self.set_status(409)
        self.write(tornado.escape.json_encode(response[1]))

class UserProfileHandler(tornado.web.RequestHandler):
    def get(self, nickname):
        data = {'nickname': nickname}

        response = user_service.get(data)
        if response[0] != True:
            self.set_status(200)
        else:
            self.set_status(404)
        self.write(tornado.escape.json_encode(response[1]))

    def post(self, nickname):
        self.set_header("Content-Type", "application/json")
        data = tornado.escape.json_decode(self.request.body)
        data.update({'nickname': nickname})

        errors = user_service.check_errors(data)
        print(errors)

        if errors[1]:
            self.set_status(404)
            error_result = {'message': "Can't find user"}
            self.write(tornado.escape.json_encode(error_result))
            return
        elif errors[0]:
            self.set_status(409)
            user_id = user_service.get_user_id(nickname)[0]
            error_result = {'message': "Can't find user with id #{id}\n".format(id=user_id)}
            self.write(tornado.escape.json_encode(error_result))
            return

        self.set_status(200)
        self.write(tornado.escape.json_encode(user_service.update(data)))