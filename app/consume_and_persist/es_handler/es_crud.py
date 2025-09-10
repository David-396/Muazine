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

    # create an index if not exist with setting mappings
    def create_index(self, index_name: str, mappings: dict):
        try:
            if self.client.indices.exists(index=index_name):
                logger.warning(f'trying to create index - "{index_name}" but index already exists.')

                return

            logger.info(f'"{index_name}" index not exist, creating new index.')

            self.client.indices.create(index=index_name, mappings=mappings)

            self.refresh(index_name=index_name)

        except Exception as e:
            logger.error(f'failed to create index - "{index_name}" ---- exception:{e}.')

    # delete an index
    def delete_index(self, index_name: str):
        try:
            if not self.client.indices.exists(index=index_name):
                logger.warning(f'trying to delete index - "{index_name}" index not exist.')
                return

            logger.info(f'"{index_name}" index exist, deleting.')

            self.client.indices.delete(index=index_name)

        except Exception as e:
            logger.error(f'failed to delete index - "{index_name}" ---- exception:{e}.')


    ''' C - create: '''
    # index one doc to es with given id
    def index_one_with_id(self, index_name:str, doc:dict, id_:str):
        try:
            res = self.client.index(index=index_name, document=doc, id=id_)
            _id = res['_id']

            logger.info(f'index succeed, _id:{_id}\ndoc: {doc}')

            self.refresh(index_name=index_name)

            return _id

        except Exception as e:
            logger.error(f'failed to index doc: {doc} ---- exception:{e}.')

    # index list of docs
    def index_many(self, index_name:str, docs:list):
        try:
            docs_to_index = []

            for doc in docs:
                temp_doc = {'_op_type': 'index', '_index': index_name, '_source': doc}

                docs_to_index.append(temp_doc)

            success, failed = helpers.bulk(self.client, docs_to_index)

            logger.info(f'{success} docs indexed, {failed} failed.')

            self.refresh(index_name=index_name)

        except Exception as e:
            logger.error(f'exception occurred in indexing_many : {e}.')
