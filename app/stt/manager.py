import time

from kafka_config import get_producer_config, get_consumer
from stt_convert import Stt
import logger

logger = logger.Logger().get_logger()

class Manager:
    def __init__(self, kafka_host:str,
                 kafka_port:str,
                 consume_topics:list[str],
                 group_id:str,
                 send_topic:str,
                 metadata_col:str,
                 recognized_text_col:str,
                 file_name_col:str,
                 absolute_path_col:str):

        self.__producer = get_producer_config(host=kafka_host, port=kafka_port)
        self.__consumer = get_consumer(topics=consume_topics, group_id=group_id, kafka_host=kafka_host, kafka_port=kafka_port)
        self.__speech_recognizer = Stt()
        self.send_topic = send_topic
        self.metadata_col = metadata_col
        self.recognized_text_col = recognized_text_col
        self.file_name_col = file_name_col
        self.absolute_path_col = absolute_path_col

    # yielding one message every iteration
    def get_message(self):
        try:
            print('starting consuming..')
            while True:

                records = self.__consumer.poll(timeout_ms=1000, max_records=1)
                for tp, messages in records.items():

                    for message in messages:
                        print(f'consume message: {message.value}')
                        yield message.value

                time.sleep(0.1)

        except Exception as e:
            logger.error(f'failed to consume messages, exception: {e}')

    # main func - consume json and produce json with the recognized text
    def run(self):
        sum_sent = 0
        try:
            messages_itr = self.get_message()
            for msg in messages_itr:
                logger.info(f'consume filename: {msg[self.metadata_col][self.file_name_col]} , extract text...')

                recognized_text = self.__speech_recognizer.recognize(file_path=msg[self.absolute_path_col])
                msg[self.metadata_col][self.recognized_text_col] = recognized_text.lower()

                self.__producer.send(topic=self.send_topic, value=msg)

                logger.info(f'{msg[self.metadata_col][self.file_name_col]} json with stt sent successfully to topic: "{self.send_topic}"')

                sum_sent += 1

            logger.info(f'{sum_sent} messages with the recognized text sent to topic: "{self.send_topic}"')

            self.__producer.flush()
            self.__producer.close()

        except Exception as e:
            logger.error(f'exception occurred in run manager, exception: {e}')
