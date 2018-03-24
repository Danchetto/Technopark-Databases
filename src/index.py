import tornado.ioloop
import tornado.web
import postgresql
from src.urls import *

PORT = 5000

def make_app():
    return tornado.web.Application(urls)

app = make_app()
app.listen(PORT)
tornado.ioloop.IOLoop.current().start()

