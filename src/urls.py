from src.controllers.UserControllers import *
from src.controllers.ForumControllers import *
from src.controllers.ThreadControllers import *
from src.controllers.PostControllers import *
from src.controllers.ServiceControllers import *
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
    (r"/thread/(?P<slug_or_id>[^/]+?)/vote", ThreadVoteHandler),
    (r"/thread/(?P<slug_or_id>[^/]+?)/posts", ThreadPostsHandler),

    (r"/post/(?P<id>[^/]+?)/details", PostDetailsHandler),

    (r"/service/clear", ClearHandler),
    (r"/service/status", StatusHandler),
]
