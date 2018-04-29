from tornado import ioloop, escape
import json, datetime
import tornado.web
from urls import *

PORT = 5000


def make_app():
    return tornado.web.Application(urls)


app = make_app()
app.listen(PORT)
# DT_HANDLER = lambda obj: obj.isoformat() if isinstance(obj, datetime.datetime) or isinstance(obj, datetime.date) else None
#
#
# def json_encode(value):
#     return json.dumps(value, default=DT_HANDLER).replace("</", "<\/")
#
#
# escape.json_encode = json_encode
ioloop.IOLoop.current().start()
