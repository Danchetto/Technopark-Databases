from src.controllers.UserControllers import *
from src.controllers.ForumControllers import *
from src.controllers.ThreadControllers import *
from src.controllers.PostControllers import *
from . import MainHandler

urls = [
    (r"/", MainHandler),

    (r"/user/(?P<nickname>[^/]+?)/create", UserCreateHandler),
    (r"/user/(?P<nickname>[^/]+?)/profile", UserProfileHandler),

    (r"/forum/create", ForumCreateHandler),
    (r"/forum/(?P<slug>[^/]+?)/create", ThreadCreateHandler),
    (r"/forum/(?P<slug>[^/]+?)/details", ForumDetailsHandler),
    (r"/forum/(?P<slug>[^/]+?)/threads", ForumThreadsHandler),

    (r"/thread/(?P<slug_or_id>[^/]+?)/create", PostCreateHandler),
    (r"/thread/(?P<slug_or_id>[^/]+?)/details", ThreadDetailsHandler),
]
