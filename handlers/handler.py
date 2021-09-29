from tornado.web import RequestHandler
import json


class AppHandler(RequestHandler):
    def set_headers(self, *args, **kwargs):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS")
        self.set_header("Content-Type", "application/json")

    def write_response(self, status_code, response=None, message=None):
        self.set_status(status_code)
        if response:
            self.finish(json.dumps(response))
        if message:
            self.finish(json.dumps({
                "message": message
            }))
        if status_code:
            self.finish(json.dumps({
                "code": status_code
            }))

    def write_error(self, status_code, **kwargs):
        self.finish(json.dumps({
            "message": {
                "code": status_code,
                "message": self._reason
            }
        }))
