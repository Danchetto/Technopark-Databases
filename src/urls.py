from controllers.UserControllers import *
from controllers.ForumControllers import *
from controllers.ThreadControllers import *
from controllers.PostControllers import *
from controllers.ServiceControllers import *

urls = [
    (r"/api/user/(?P<nickname>[^/]+?)/create", UserCreateHandler),
    (r"/api/user/(?P<nickname>[^/]+?)/profile", UserProfileHandler),

    (r"/api/forum/create", ForumCreateHandler),
    (r"/api/forum/(?P<slug>[^/]+?)/create", ThreadCreateHandler),
    (r"/api/forum/(?P<slug>[^/]+?)/details", ForumDetailsHandler),
    (r"/api/forum/(?P<slug>[^/]+?)/threads", ForumThreadsHandler),
    (r"/api/forum/(?P<slug>[^/]+?)/users", ForumUsersHandler),

    (r"/api/thread/(?P<slug_or_id>[^/]+?)/create", PostCreateHandler),
    (r"/api/thread/(?P<slug_or_id>[^/]+?)/details", ThreadDetailsHandler),
    (r"/api/thread/(?P<slug_or_id>[^/]+?)/vote", ThreadVoteHandler),
    (r"/api/thread/(?P<slug_or_id>[^/]+?)/posts", ThreadPostsHandler),

    (r"/api/post/(?P<id>[^/]+?)/details", PostDetailsHandler),

    (r"/api/service/clear", ClearHandler),
    (r"/api/service/status", StatusHandler),
]
