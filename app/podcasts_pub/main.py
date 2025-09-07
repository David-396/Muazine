import logging
import os
from manager import Manager

logging.basicConfig(level=logging.INFO,format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',handlers=[logging.FileHandler("main.log"),logging.StreamHandler()])


KAFKA_HOST = os.getenv('KAFKA_HOST', 'localhost')
KAFKA_PORT = os.getenv('KAFKA_PORT', '9092')
FILES_DIR_PATH = os.getenv('FILES_DIR_PATH', r'..\..\podcasts')
SEND_TOPIC = os.getenv('SEND_TOPIC', 'files_json')
BATCHES = os.getenv('BATCHES', 5)

logging.info(f'getting the environment variables.')

logging.info(f'creating manager instance.')
manager = Manager(kafka_host=KAFKA_HOST,kafka_port=KAFKA_PORT)

logging.info(f'running the manager.')
manager.run(files_dir_path=FILES_DIR_PATH,
            send_topic=SEND_TOPIC,
            batches=BATCHES)