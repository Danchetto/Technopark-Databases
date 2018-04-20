import tornado.web, tornado.escape
from src.services.ServiceService import service_service

class ClearHandler(tornado.web.RequestHandler):
    def post(self):
        self.set_header("Content-Type", "application/json")
        self.set_status(200)
        self.write(tornado.escape.json_encode({'message': 'Done!'}))
        service_service.clear()
        return


class StatusHandler(tornado.web.RequestHandler):
    def get(self):
        self.set_header("Content-Type", "application/json")
        self.set_status(200)
        self.write(tornado.escape.json_encode(service_service.status()))
        return