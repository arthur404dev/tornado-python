from logging import debug
from tornado.web import Application
from tornado.ioloop import IOLoop
from tornado.httpserver import HTTPServer
from logzero import logger

from handlers.metricas import MetricasHandler, CalculaMetricasHandler, RetornaMetricasHandler
from persistence.database import mongo

import config.settings as settings


def make_app():
    endpoints = [
        (r"/api/calcula_metricas", CalculaMetricasHandler),
        (r"/api/retorna_metricas", RetornaMetricasHandler),
        (r"/api/metricas", MetricasHandler)
    ]
    return Application(
        endpoints,
        debug=True,
        mongo=mongo.MongoDB(),
    )


if __name__ == "__main__":
    app = make_app()
    settings.init_logs()
    server = HTTPServer(app)
    server.listen(int(settings.PORT))
    logger.info('Server is online listening on port {0}'.format(
        settings.PORT))
    IOLoop.current().start()
