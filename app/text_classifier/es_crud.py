from elasticsearch import Elasticsearch, helpers
from logger import Logger

logger = Logger.get_logger()



class CRUD:
    def __init__(self, es_client:Elasticsearch):
        self.client = es_client

    # refresh the es
    def refresh(self, index_name: str):
        try:
            self.client.indices.refresh(index=index_name)

        except Exception as e:
            logger.error(f'failed to refresh, exception: {e}')

    # get docs by specific query
    def get_by_query(self, index_name:str, query:dict, size:int=1000):
        try:
            logger.info(f'retrieving docs by query: {query}')

            docs = self.client.search(index=index_name,body=query, size=size)["hits"]["hits"]

            return docs

        except Exception as e:
            logger.error(f'exception occurred to extract docs, exception:{e}.')
