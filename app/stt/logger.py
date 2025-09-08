import logging
import os
from dotenv import load_dotenv
from elasticsearch import Elasticsearch
from datetime import datetime

load_dotenv()

LOGGER_NAME = os.getenv('LOGGER_NAME')
LOGGER_INDEX_NAME = os.getenv('LOGGER_INDEX_NAME')
ES_HOST = os.getenv('ES_HOST')
ES_PORT = os.getenv('ES_PORT')

class Logger:
    _logger = None

    @classmethod
    def get_logger(cls, name=LOGGER_NAME, es_host=ES_HOST, es_port=ES_PORT, index=LOGGER_INDEX_NAME, level=logging.DEBUG):
        if cls._logger:
            return cls._logger

        logger = logging.getLogger(name)
        logger.setLevel(level)

        if not logger.handlers:
            es_uri = f'http://{es_host}:{es_port}'
            es = Elasticsearch(es_uri)

            class ESHandler(logging.Handler):
                def emit(self, record):
                    try:
                        es.index(index=index, document={"timestamp": datetime.utcnow().isoformat(),
                                                        "level": record.levelname,
                                                        "logger": record.name,
                                                        "message": record.getMessage()
                                                        })

                    except Exception as e:
                        print(f"ES log failed: {e}")

            logger.addHandler(ESHandler())
            logger.addHandler(logging.StreamHandler())

        cls._logger = logger
        return logger