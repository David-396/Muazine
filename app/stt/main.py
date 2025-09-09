import os
from dotenv import load_dotenv

from app.stt import stt_convert
from manager import Manager
from logger import Logger

logger = Logger.get_logger()


load_dotenv()

KAFKA_HOST = os.getenv('KAFKA_HOST')
KAFKA_PORT = os.getenv('KAFKA_PORT')
GROUP_ID = os.getenv('GROUP_ID')
SEND_TOPIC = os.getenv('SEND_TOPIC')

CONSUME_TOPICS=['files_json']

logger.info('init the stt manager..')

manager = Manager(kafka_host=KAFKA_HOST,
                  kafka_port=KAFKA_PORT,
                  consume_topics=CONSUME_TOPICS,
                  group_id=GROUP_ID,
                  send_topic=SEND_TOPIC
                  )

logger.info('running the manager..')

manager.run()