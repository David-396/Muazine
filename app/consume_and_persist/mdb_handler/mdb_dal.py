from pymongo import MongoClient
from consume_and_persist.logger import Logger

logger = Logger.get_logger()

class MongoConnector:
    def __init__(self, mongo_host:str, mongo_port:int, mongo_username:str, mongo_pass:str):
        self.__client = MongoClient(
            host=mongo_host,
            port=mongo_port,
            username=mongo_username,
            password=mongo_pass
        )

        logger.info(f'new mongo connection on {self.__client.address}')

    # return the client object
    def get_client(self):
         return self.__client

    # close the client connection
    def close(self):
        try:
            logger.info(f'closing mongo connection on {self.__client.address}')
            self.__client.close()

        except Exception as e:
            logger.error(f'failed to close mongo client connection, exception: {e}')

    # for with statement
    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
