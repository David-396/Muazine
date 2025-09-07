import os
import manager
import logging

ES_HOST = os.getenv('ES_HOST','localhost')
ES_PORT = os.getenv('ES_PORT', '9200')
ES_INDEX = os.getenv('ES_INDEX', 'json_files_metadata')
MDB_DB_NAME = os.getenv('MDB_DB_NAME', 'podcasts_persister')
MDB_COLL_NAME = os.getenv('MDB_COLL_NAME', 'podcasts_content')
MONGO_HOST = os.getenv("MONGO_HOST", "localhost")
MONGO_PORT = int(os.getenv("MONGO_PORT", '27017'))
MONGO_USER = os.getenv("MONGO_USER", "root")
MONGO_PASSWORD = os.getenv("MONGO_PASSWORD", "pass")

logging.basicConfig(level=logging.INFO,format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',handlers=[logging.FileHandler("main.log"),logging.StreamHandler()])


m = manager.Manager(topics=['files_json'],
                    group_id='consume_files_json',
                    kafka_host='localhost',
                    kafka_port='9092',
                    es_host=ES_HOST,
                    es_port=ES_PORT,
                    es_index=ES_INDEX,
                    mdb_db_name=MDB_DB_NAME,
                    mdb_coll_name=MDB_COLL_NAME,
                    mongo_host=MONGO_HOST,
                    mongo_port=MONGO_PORT,
                    mongo_username=MONGO_USER,
                    mongo_pass=MONGO_PASSWORD)
m.run()

# with mdb_handler.mdb_dal.MongoConnector(mongo_host=MONGO_HOST, mongo_port=MONGO_PORT, mongo_username=None,
#                             mongo_pass=None) as mdb_dal_obj:
#     mdb_crud_obj = mdb_handler.mdb_crud.MongoCRUD(mdb_dal_obj.get_client())
#
#     a = mdb_crud_obj.save_audio_content_file_on_mdb(db_name=MDB_DB_NAME,
#                                                     collection_name=MDB_COLL_NAME,
#                                                     custom_id=1,
#                                                     audio_file_path=r'C:\Users\User\Desktop\Muazine\podcasts\download.wav',
#                                                     file_name='download.wav')
#
#     print(a)

