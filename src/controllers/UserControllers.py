import tornado.web, tornado.escape
from src.services.UserService import UserService
import json

class UserCreateHandler(tornado.web.RequestHandler):
    def get(self, nickname):
        self.write("Hello, " + nickname)

    def post(self, nickname):
        self.set_header("Content-Type", "application/json")
        data = tornado.escape.json_decode(self.request.body)
        data.update({'nickname': nickname})
        user_serv = UserService()
        user_serv.user_create(data)
