from src.controllers.UserControllers import *
from . import MainHandler

urls = [
    (r"/", MainHandler),
    (r"/user/(?P<nickname>[^/]+?)/create", UserCreateHandler),
    (r"/user/(?P<nickname>[^/]+?)/profile", UserProfileHandler)
]
