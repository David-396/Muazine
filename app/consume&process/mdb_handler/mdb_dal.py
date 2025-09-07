from pymongo import MongoClient
import logging

logging.basicConfig(level=logging.DEBUG,format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',handlers=[logging.FileHandler("mdb_dal.log"),logging.StreamHandler()])


class MongoConnector:
    def __init__(self, mongo_host:str, mongo_port:int, mongo_username:str, mongo_pass:str):
        self.__client = MongoClient(
            host=mongo_host,
            port=mongo_port,
            username=mongo_username,
            password=mongo_pass
        )

        logging.info(f'new mongo connection on {self.__client.address}')


    def get_client(self):
         return self.__client


    # for with statement
    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        logging.info(f'closing mongo connection on {self.__client.address}')
        self.__client.close()
