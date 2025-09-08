import logging
import os
from manager import Manager
from dotenv import load_dotenv
from app.logger import Logger

logger = Logger.get_logger()
logging.basicConfig(level=logging.INFO,format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',handlers=[logging.FileHandler("files_meta_pub.log"),logging.StreamHandler()])

load_dotenv()

KAFKA_HOST = os.getenv('KAFKA_HOST')
KAFKA_PORT = os.getenv('KAFKA_PORT')
FILES_DIR_PATH = os.getenv('FILES_DIR_PATH')
SEND_TOPIC = os.getenv('SEND_TOPIC')
BATCHES = int(os.getenv('BATCHES'))


manager = Manager(kafka_host=KAFKA_HOST,kafka_port=KAFKA_PORT)

logging.info(f'running the files_meta_pub manager.')
logger.info(f'running the files_meta_pub manager.')

manager.run(files_dir_path=FILES_DIR_PATH,
            send_topic=SEND_TOPIC,
            batches=BATCHES)