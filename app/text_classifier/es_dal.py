from elasticsearch import Elasticsearch
from logger import Logger

logger = Logger.get_logger()

class ESConnector:
    def __init__(self, host:str, port:str|int):
        self.__es_uri =  f'http://{host}:{port}'
        self.__client = Elasticsearch(self.__es_uri)

        logger.info(f'creating new es client on - {self.__es_uri}.')


    # return the es client
    def get_client(self):
        return self.__client

    # check connection status
    def ping(self):
        try:
            connected = self.__client.ping()
            msg = 'ping result - connection to es succeed.' if connected else 'ping result - connection to es failed!'
            logger.info(msg)
            return connected

        except Exception as e:
            logger.error(f'exception occurred to ping to es client, exception: {e}')
            return False

    # closing the es connection
    def _close(self):
        try:
            self.__client.close()
            logger.info(f'elastic connection successfully closed on - {self.__es_uri}.')

        except Exception as e:
            logger.error(f'exception occurred in closing es client. exception: {e}.')


    # for with statement
    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        self._close()