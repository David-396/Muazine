from elasticsearch import Elasticsearch, helpers
from app.consume_and_persist.logger import Logger

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

    ''' R - read '''
    # get only one doc by id
    def get_doc_by_id(self, index_name:str, doc_id:str):
        try:
            doc = self.client.get(index=index_name, id=doc_id)

            return doc

        except Exception as e:
            logger.error(f'exception occurred to get id {doc_id}, exception: {e}.')

    # return all docs from index
    def get_all_docs(self, index_name:str, size:int=10000):
        try:

            docs = self.client.search(index=index_name, size=size)["hits"]["hits"]

            return docs

        except Exception as e:
            logger.error(f'exception occurred to extract docs, exception:{e}.')

    # get docs by specific query
    def get_by_query(self, index_name:str, query:dict, size:int):
        try:
            logger.info(f'retrieving docs by query: {query}')

            docs = self.client.search(index=index_name,body=query, size=size)["hits"]["hits"]

            return docs

        except Exception as e:
            logger.error(f'exception occurred to extract docs, exception:{e}.')


    ''' U - update '''
    # update one doc by id to known value
    def update_one_by_id(self, index_name:str, doc_id:str, doc_update_part:dict):
        try:
            self.client.update(index=index_name, id=doc_id, doc=doc_update_part)

            logger.info(f'doc id: {doc_id}, successfully updated.')

            self.refresh(index_name=index_name)

        except Exception as e:
            logger.error(f'failed to update doc with id: {doc_id}, exception: {e}.')

    # update many by list of ids and list of the action part with the value in the update part
    def update_many_by_id(self, index_name:str, docs_ids:list, docs_update_part:list):
        try:
            if len(docs_ids) != len(docs_update_part):
                logger.critical(f'to bulk docs docs_ids and docs_update_part lists should be with the same len(), docs_ids len: {len(docs_ids)}, docs_update_part len: {len(docs_update_part)}.')
                return

            docs_to_update = []

            for i in range(len(docs_ids)):
                temp_update_doc = {'_op_type': 'update', '_index': index_name, '_id':docs_ids[i], 'doc':docs_update_part[i]}
                docs_to_update.append(temp_update_doc)

            success, failed = helpers.bulk(client=self.client, actions=docs_to_update)

            logger.info(f'{success} docs successfully updated and {failed} docs failed.')

            self.refresh(index_name=index_name)

        except Exception as e:
            logger.error(f'exception in update_many_by_id() failed to update docs, exception: {e}.')

    # update the docs by a given query
    def update_by_query(self, index_name:str, query:dict):
        try:
            res = self.client.update_by_query(index=index_name,body=query)

            logger.info(f'update succeed, response from es: {res}.')

            self.refresh(index_name=index_name)
            return res

        except Exception as e:
            logger.error(f'exception occurred in update by query, exception: {e}')


    ''' D - delete '''
    # delete one doc by id
    def delete_one_by_id(self, index_name:str, doc_id:str):
        try:
            self.client.delete(index=index_name, id=doc_id)

            logger.info(f'doc id: {doc_id}, successfully deleted.')

            self.refresh(index_name=index_name)

        except Exception as e:
            logger.error(f'failed to delete doc with id: {doc_id}, exception: {e}.')

    # delete many by list of ids
    def delete_many_by_id(self, index_name:str, docs_ids:list):
        try:

            docs_to_delete = []

            for doc_id in docs_ids:
                temp_delete_doc = {'_op_type': 'delete', '_index': index_name, '_id':doc_id}
                docs_to_delete.append(temp_delete_doc)

            success, failed = helpers.bulk(client=self.client, actions=docs_to_delete)

            logger.info(f'{success} docs successfully deleted and {failed} docs failed.')

            self.refresh(index_name=index_name)

        except Exception as e:
            logger.error(f'exception in delete_many_by_id() failed to delete docs, exception: {e}.')

    # delete the docs by a given query
    def delete_by_query(self, index_name:str, query:dict):
        try:
            res = self.client.delete_by_query(index=index_name,body=query)

            logger.info(f'delete succeed, response from es: {res}.')

            self.refresh(index_name=index_name)
            return res

        except Exception as e:
            logger.error(f'exception occurred in delete by query, exception: {e}')