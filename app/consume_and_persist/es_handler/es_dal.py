import logging
from elasticsearch import Elasticsearch
from app.logger import Logger


logger = Logger.get_logger()
logging.basicConfig(level=logging.INFO,format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',handlers=[logging.FileHandler("consume_and_persist.log"),logging.StreamHandler()])

class ESConnector:
    def __init__(self, host:str, port:str|int):
        self.__es_uri =  f'http://{host}:{port}'
        self.__client = Elasticsearch(self.__es_uri)

        logging.info(f'creating new es client on - {self.__es_uri}.')
        logger.info(f'creating new es client on - {self.__es_uri}.')


    # return the es client
    def get_client(self):
        return self.__client

    # check connection status
    def ping(self):
        try:
            connected = self.__client.ping()
            msg = 'connection to es succeed.' if connected else 'connection to es failed!'
            logging.info(msg)
            return connected

        except Exception as e:
            logging.critical(f'exception occurred to ping to es client, exception: {e}')
            logger.error(f'exception occurred to ping to es client, exception: {e}')
            return False

    # closing the es connection
    def _close(self):
        try:
            self.__client.close()
            logging.info(f'elastic connection successfully closed on - {self.__es_uri}.')
            logger.info(f'elastic connection successfully closed on - {self.__es_uri}.')

        except Exception as e:
            logging.critical(f'exception occurred in closing es client. exception: {e}.')
            logger.error(f'exception occurred in closing es client. exception: {e}.')


    # for with statement
    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        self._close()