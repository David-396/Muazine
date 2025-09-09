from kafka import KafkaProducer, KafkaConsumer
import json
from logger import Logger

logger = Logger.get_logger()

# setting the producer
def get_producer_config(host:str, port:str):
    try:

        bootstrap_servers = [f'{host}:{port}']
        producer = KafkaProducer(bootstrap_servers=bootstrap_servers,
                                 value_serializer=lambda x: json.dumps(x).encode('utf-8'))

        logger.info(f'creating new kafka producer on {bootstrap_servers}.')

        return producer

    except Exception as e:
        logger.error(f'failed occurred on producer creating, exception: {e}')


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