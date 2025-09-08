from kafka import KafkaConsumer
import json
from consume_and_persist.logger import Logger

logger = Logger.get_logger()

# setting the consumer
def get_consumer(topics:list[str], group_id:str, kafka_host:str, kafka_port:str):
    logger.info(f"creating new consumer on topics: {topics}")

    bootstrap_servers = [f'{kafka_host}:{kafka_port}']
    consumer = KafkaConsumer(group_id=group_id,
                             value_deserializer=lambda m: json.loads(m.decode('utf-8')),
                             bootstrap_servers=bootstrap_servers,
                             auto_offset_reset='earliest')

    consumer.subscribe(topics=topics)

    return consumer