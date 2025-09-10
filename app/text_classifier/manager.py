from logger import Logger
from classifier import Classifier
from es_dal import ESConnector
from es_crud import CRUD
from elasticsearch.helpers import bulk

logger = Logger().get_logger()


class Manager:
    def __init__(self,
                 es_host:str,
                 es_port:str|int,
                 es_index, hostile_lst:list,
                 less_hostile_lst:list,
                 percent_is_bds_threshold:float,
                 risk_binds:list[float]):

        self.es_host = es_host
        self.es_port = es_port
        self.es_index = es_index

        self.classifier = Classifier(hostile_list=hostile_lst,
                                     less_hostile_list=less_hostile_lst,
                                     percent_is_bds_threshold=percent_is_bds_threshold,
                                     risk_binds=risk_binds)

        self.hostile_lst = hostile_lst
        self.less_hostile_lst = less_hostile_lst
        self.percent_is_bds_threshold = percent_is_bds_threshold
        self.risk_binds = risk_binds


    # classify the docs
    def run_classifier(self):
        try:
            with ESConnector(host=self.es_host, port=self.es_port) as es_client:
                es_crud = CRUD(es_client=es_client.get_client())

                query = {
                    "query": {
                        "bool": {
                            "must": [{"match": {"metadata.risk_rank": "unprocessed"}}],
                            "should": [{"match": {"metadata.recognized_text": ' '.join(self.hostile_lst) + ' ' + ' '.join(self.less_hostile_lst)}}]
                        }
                    },
                    "highlight": {
                        "fields": {
                            "metadata.recognized_text": {}
                        }
                    }
                }

                hostile_and_less_hostile_docs = es_crud.get_by_query(index_name=self.es_index, query=query)

                bulk_actions = []

                temp_action = {'_op_type': 'update',
                               '_index': self.es_index,
                               'doc':{'metadata':{}}}

                if hostile_and_less_hostile_docs:
                    for doc in hostile_and_less_hostile_docs:

                        if 'bds_percent' not in doc['_source']['metadata'].keys():

                            bds_percent = self.classifier.bds_percent(result_doc=doc)

                            temp_action['doc']['metadata']['bds_percent']  = bds_percent
                            temp_action['doc']['metadata']['is_bds'] =  self.classifier.is_bds(percent=bds_percent)
                            temp_action['doc']['metadata']['risk_rank'] = self.classifier.risk_rank(percent=bds_percent)

                            temp_action['_id'] = doc['_id']

                            # es_crud.client.update(index=self.es_index, id=doc['_id'], doc=temp_action)

                            bulk_actions.append(temp_action)

                            logger.info(f'doc id:{doc['_id']} successfully classified - result: {temp_action['doc']}')

                    if bulk_actions:
                        success, failed = bulk(client=es_client.get_client(), actions=bulk_actions)
                        es_crud.refresh(index_name=self.es_index)

                        logger.info(f'{success} docs updated successfully and - {failed} - has failed.')

        except Exception as e:
            logger.error(f'failed to run the classifier manager, exception: {e}')