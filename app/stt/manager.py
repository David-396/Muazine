from kafka_config import get_producer_config, get_consumer
from stt_convert import Stt
import logger

logger = logger.Logger().get_logger()

class Manager:
    def __init__(self, kafka_host:str, kafka_port:str, consume_topics:list[str], group_id:str, send_topic:str):
        self.__producer = get_producer_config(host=kafka_host, port=kafka_port)
        self.__consumer = get_consumer(topics=consume_topics, group_id=group_id, kafka_host=kafka_host, kafka_port=kafka_port)
        self.__speech_recognizer = Stt()
        self.send_topic = send_topic

    # yielding one message every iteration
    def get_message(self):

        while True:
            records = self.__consumer.poll(timeout_ms=1000, max_records=1)
            for tp, messages in records.items():

                for message in messages:
                    yield message.value


    # main func - consume json and produce json with the recognized text
    def run(self):
        sum_sent = 0
        try:
            messages_itr = self.get_message()
            for msg in messages_itr:
                recognized_text = self.__speech_recognizer.recognize(file_path=msg['absolute_path'])
                msg['metadata']['recognized_text'] = recognized_text

                self.__producer.send(topic=self.send_topic, value=msg)

                logger.info(f'{msg['metadata']['name']} json with stt sent successfully to topic: "{self.send_topic}"')

                sum_sent += 1

            logger.info(f'{sum_sent} messages with the recognized text sent to topic: "{self.send_topic}"')

            self.__producer.flush()

        except Exception as e:
            logger.error(f'exception occurred in run manager, exception: {e}')
