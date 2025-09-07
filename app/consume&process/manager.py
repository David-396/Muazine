import hashlib
import logging
from kafka_handler import consumer_config
from es_handler import es_crud, es_dal
from mdb_handler import mdb_crud, mdb_dal


logging.basicConfig(level=logging.INFO,format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',handlers=[logging.FileHandler("manager.log"),logging.StreamHandler()])


class Manager:
    def __init__(self,
                 topics:list[str],
                 group_id:str,
                 kafka_host:str,
                 kafka_port:str,
                 es_host:str,
                 es_port:str,
                 es_index:str,
                 mdb_db_name:str,
                 mdb_coll_name:str,
                 mongo_host:str,
                 mongo_port:int,
                 mongo_username:str,
                 mongo_pass:str):

        self.__consumer = consumer_config.get_consumer(topics=topics,group_id=group_id,kafka_host=kafka_host,kafka_port=kafka_port)
        self.es_host = es_host
        self.es_port = es_port
        self.es_index = es_index
        self.mdb_db_name = mdb_db_name
        self.mdb_coll_name = mdb_coll_name
        self.mongo_host = mongo_host
        self.mongo_port = mongo_port
        self.mongo_username = mongo_username
        self.mongo_pass = mongo_pass



    # hashing a str to big int
    @staticmethod
    def str_hash(string: str):
        encoded_string = string.encode('utf-8')
        return str(int(hashlib.sha256(encoded_string).hexdigest(), 16))

    # yielding one message every iteration
    def get_message(self):

        while True:
            records = self.__consumer.poll(timeout_ms=1000, max_records=1)
            for tp, messages in records.items():

                for message in messages:
                    yield message.value

    # main run
    def run(self):
        try:
            logging.info('running the es , mdb persister')

            with es_dal.ESConnector(host=self.es_host,port=self.es_port) as es_dal_obj:
                es_crud_obj = es_crud.CRUD(es_client=es_dal_obj.get_client())

                with mdb_dal.MongoConnector(mongo_host=self.mongo_host,mongo_port=self.mongo_port,mongo_username=self.mongo_username,mongo_pass=self.mongo_pass) as mdb_dal_obj:
                    mdb_crud_obj = mdb_crud.MongoCRUD(mdb_dal_obj.get_client())


                    consumer_iterator = self.get_message()
                    for msg in consumer_iterator:
                        file_name = msg['metadata']['name']
                        hashed_id = self.str_hash(file_name)

                        es_crud_obj.index_one_with_id(index_name=self.es_index, doc=msg, id_=hashed_id)

                        msg['_id'] = hashed_id
                        mdb_crud_obj.save_audio_content_file_on_mdb(db_name=self.mdb_db_name,
                                                                    collection_name=self.mdb_coll_name,
                                                                    custom_id=hashed_id,
                                                                    audio_file_path=msg['absolute_path'],
                                                                    file_name=file_name)


        except Exception as e:
            logging.critical(f'failed to run the manager , exception: {e}')


