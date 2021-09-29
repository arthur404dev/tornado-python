import os
import logging
import logzero
from dotenv import load_dotenv

load_dotenv()

PORT = os.environ.get("PORT")
MONGO_URI = os.environ.get("MONGO_URI")
METRICAS_DATABASE = os.environ.get("METRICAS_DATABASE")
METRICAS_COLL_INPUT = os.environ.get("METRICAS_COLL_INPUT")
METRICAS_COLL_OUTPUT = os.environ.get("METRICAS_COLL_OUTPUT")


def init_logs():
    logzero.logfile("logs.log", maxBytes=9999999,
                    backupCount=3, loglevel=logging.ERROR)
    formatter = logging.Formatter('%(asctime)s-%(levelname)s=%(message)s')
    logzero.formatter(formatter)
