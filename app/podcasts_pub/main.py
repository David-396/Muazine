import logging
import os
from manager import Manager
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO,format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',handlers=[logging.FileHandler("main.log"),logging.StreamHandler()])

load_dotenv()

KAFKA_HOST = os.getenv('KAFKA_HOST')
KAFKA_PORT = os.getenv('KAFKA_PORT')
FILES_DIR_PATH = os.getenv('FILES_DIR_PATH')
SEND_TOPIC = os.getenv('SEND_TOPIC')
BATCHES = int(os.getenv('BATCHES'))

logging.info(f'getting the environment variables.')

logging.info(f'creating manager instance.')

manager = Manager(kafka_host=KAFKA_HOST,kafka_port=KAFKA_PORT)

logging.info(f'running the manager.')

manager.run(files_dir_path=FILES_DIR_PATH,
            send_topic=SEND_TOPIC,
            batches=BATCHES)