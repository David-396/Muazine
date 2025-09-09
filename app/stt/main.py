import os
from dotenv import load_dotenv
from manager import Manager
from logger import Logger

logger = Logger.get_logger()


load_dotenv()

KAFKA_HOST = os.getenv('KAFKA_HOST')
KAFKA_PORT = os.getenv('KAFKA_PORT')
GROUP_ID = os.getenv('GROUP_ID')
SEND_TOPIC = os.getenv('SEND_TOPIC')
METADATA_COL = os.getenv('METADATA_COL')
RECOGNIZED_TEXT_COL = os.getenv('RECOGNIZED_TEXT_COL')
FILE_NAME_COL = os.getenv('FILE_NAME_COL')
ABSOLUTE_PATH_COL = os.getenv('ABSOLUTE_PATH_COL')

CONSUME_TOPICS=['files_json']

logger.info('init the stt manager..')

manager = Manager(kafka_host=KAFKA_HOST,
                  kafka_port=KAFKA_PORT,
                  consume_topics=CONSUME_TOPICS,
                  group_id=GROUP_ID,
                  send_topic=SEND_TOPIC,
                  metadata_col=METADATA_COL,
                  recognized_text_col=RECOGNIZED_TEXT_COL,
                  file_name_col=FILE_NAME_COL,
                  absolute_path_col=ABSOLUTE_PATH_COL
                  )

logger.info('running the manager..')

'''
the stt service consume the json file data and add to the json the recognized text
the recognizer is heavy and need a service for himself
and before indexing to elastic - complete all the json data about the file and then saving to elastic
'''
manager.run()