import os
import manager
from dotenv import load_dotenv
from logger import Logger


logger = Logger.get_logger()

load_dotenv()

ES_HOST = os.getenv('ES_HOST')
ES_PORT = os.getenv('ES_PORT')
ES_INDEX = os.getenv('ES_INDEX')
# ES_INDEX_MAPPING = json.loads(os.getenv('ES_INDEX_MAPPING'))

MDB_DB_NAME = os.getenv('MDB_DB_NAME')
MDB_COLL_NAME = os.getenv('MDB_COLL_NAME')
MONGO_HOST = os.getenv("MONGO_HOST")
MONGO_PORT = int(os.getenv("MONGO_PORT"))
MONGO_USER = os.getenv("MONGO_USER") if os.getenv("MONGO_USER") != 'None' else None
MONGO_PASSWORD = os.getenv("MONGO_PASSWORD") if os.getenv("MONGO_PASSWORD") != 'None' else None

# TOPICS = json.loads(os.getenv('TOPICS'))
GROUP_ID = os.getenv('GROUP_ID')
KAFKA_HOST = os.getenv('KAFKA_HOST')
KAFKA_PORT = os.getenv('KAFKA_PORT')




ES_INDEX_MAPPING={"properties":
                           {"absolute_path":{"type":"keyword"},
                            "metadata.type":{"type":"keyword"},
                            "metadata.name":{"type":"keyword"},
                            "metadata.size_in_megabytes":{"type":"float"},
                            "metadata.created_time":{"type":"date", "format": "yyyy-MM-dd HH:mm:ss.SSSSSS"},
                            "metadata.recognized_text": {"type":"text"},
                            "metadata.bds_percent": {"type": "float"},
                            "metadata.is_bds": {"type": "boolean"},
                            "metadata.risk_rank": {"type": "keyword"}
                            }
                       }


CONSUME_TOPICS=['files_json_with_stt']

logger.info('initialize consume_and_persist manager..')

m = manager.Manager(consume_topics=CONSUME_TOPICS,
                    group_id=GROUP_ID,
                    kafka_host=KAFKA_HOST,
                    kafka_port=KAFKA_PORT,
                    es_host=ES_HOST,
                    es_port=ES_PORT,
                    es_index=ES_INDEX,
                    es_index_mapping=ES_INDEX_MAPPING,
                    mdb_db_name=MDB_DB_NAME,
                    mdb_coll_name=MDB_COLL_NAME,
                    mongo_host=MONGO_HOST,
                    mongo_port=MONGO_PORT,
                    mongo_username=MONGO_USER,
                    mongo_pass=MONGO_PASSWORD)

logger.info('run manager..')
m.run()
