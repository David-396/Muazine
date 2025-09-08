from kafka import KafkaProducer
import json
from logger import Logger

logger = Logger.get_logger()

class Producer:
    def __init__(self, host:str, port:str):
        self.host = host
        self.port = port
        self.client = self.get_producer_config()

    # create a new producer on kafka
    def get_producer_config(self):
        try:

            bootstrap_servers = [f'{self.host}:{self.port}']
            producer = KafkaProducer(bootstrap_servers=bootstrap_servers,
                                     value_serializer=lambda x: json.dumps(x).encode('utf-8'))

            logger.info(f'creating new kafka producer on {bootstrap_servers}.')

            return producer

        except Exception as e:
            logger.error(f'failed occurred on producer creating, exception: {e}')