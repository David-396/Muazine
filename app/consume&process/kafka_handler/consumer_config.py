import logging
from kafka import KafkaConsumer
import json

logging.basicConfig(level=logging.DEBUG,format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',handlers=[logging.FileHandler("consumer_config.log"),logging.StreamHandler()])


def get_consumer(topics:list[str], group_id:str, kafka_host:str, kafka_port:str):
    logging.info("Creating Consumer Object ..")

    bootstrap_servers = [f'{kafka_host}:{kafka_port}']
    consumer = KafkaConsumer(group_id=group_id,
                             value_deserializer=lambda m: json.loads(m.decode('utf-8')),
                             bootstrap_servers=bootstrap_servers,
                             auto_offset_reset='earliest')

    consumer.subscribe(topics=topics)

    return consumer