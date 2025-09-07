import logging
import os
from manager import Manager

logging.basicConfig(level=logging.DEBUG,format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',handlers=[logging.FileHandler("main.log"),logging.StreamHandler()])


KAFKA_HOST = os.getenv('KAFKA_HOST', 'localhost')
KAFKA_PORT = os.getenv('KAFKA_PORT', '9092')

manager = Manager(kafka_host=KAFKA_HOST,kafka_port=KAFKA_PORT)