from handlers.handler import AppHandler
from persistence.schemas.payload import PayloadSchema
from logzero import logger
from marshmallow import ValidationError
from http import HTTPStatus
from tornado import web
import config.settings as settings
import json


class MetricasHandler(AppHandler):
    mongo_collection: None

    def data_received(self, chunk=None):
        if self.request.body:
            return json.loads(self.request.body)

    def set_database(self, type):
        if type != 'input' or type != 'output':
            return
        if type == 'input':
            self.settings['mongo'].set_collection(
                settings.METRICAS_DATABASE, settings.METRICAS_COLL_INPUT)
        if type == 'output':
            self.settings['mongo'].set_collection(
                settings.METRICAS_DATABASE, settings.METRICAS_COLL_OUTPUT)
        self.mongo_collection = self.settings['mongo']

    def calcula_metricas(self):
        try:
            payload = PayloadSchema().load(self.data_received())
        except ValidationError as err:
            logger.error(err)
            raise web.HTTPError(
                status_code=HTTPStatus.BAD_REQUEST, reason=str(err)
            )
        else:
            try:
                # Vai calcular aqui com o pandas etc, etc utilizando o payload
                calculo = 1+1+payload
            except Exception as err:
                logger.error(err)
            else:
                try:
                    res = self.mongo_collection.insert_one(data=calculo)
                except Exception as err:
                    logger.error(err)
                    raise web.HTTPError(
                        status_code=HTTPStatus.INTERNAL_SERVER_ERROR, reason=str(err))
                else:
                    resposta = {
                        "distancia_percorrida": 1227721,
                        "tempo_em_movimento": 525353,
                        "tempo_parado": 7129127921,
                    }
                    self.write_response(HTTPStatus.OK, response=resposta)

    def retorna_metricas(self):
        try:
            self.set_database('output')
            result = self.mongo_collection.fetch_all()
        except Exception as err:
            logger.error(err)
            raise web.HTTPError(
                status_code=HTTPStatus.BAD_REQUEST, reason=str(err))
        else:
            self.write_response(HTTPStatus.OK, result)

    def get(self):
        self.retorna_metricas()

    def post(self):
        self.calcula_metricas()


class CalculaMetricasHandler(MetricasHandler):
    def get(self):
        self.retorna_metricas()


class RetornaMetricasHandler(MetricasHandler):
    def post(self):
        self.calcula_metricas()
