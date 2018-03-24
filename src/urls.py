from src.controllers.UserControllers import *
from src.controllers.ForumControllers import *
from src.controllers.ThreadControllers import *
from . import MainHandler

urls = [
    (r"/", MainHandler),
    (r"/user/(?P<nickname>[^/]+?)/create", UserCreateHandler),
    (r"/user/(?P<nickname>[^/]+?)/profile", UserProfileHandler),
    (r"/forum/create", ForumCreateHandler),
    (r"/forum/(?P<slug>[^/]+?)/create", ThreadCreateHandler),
]
