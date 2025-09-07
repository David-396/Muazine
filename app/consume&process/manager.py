import hashlib
from kafka_handler import consumer_config


class Manager:
    def __init__(self,topics:list[str], group_id:str, kafka_host:str, kafka_port:str):
        self.consumer = consumer_config.get_consumer(topics=topics,group_id=group_id,kafka_host=kafka_host,kafka_port=kafka_port)


    @staticmethod
    def str_hash(string: str):
        encoded_string = string.encode('utf-8')
        return int(hashlib.sha256(encoded_string).hexdigest(), 16)

