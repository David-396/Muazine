import logging
import time

from producer_config import Producer
from file_meta_made import FileMetaMade
from pathlib import Path

logging.basicConfig(level=logging.DEBUG,format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',handlers=[logging.FileHandler("manager.log"),logging.StreamHandler()])

class Manager:
    def __init__(self, kafka_host:str, kafka_port:str):
        self.producer = Producer(host=kafka_host, port=kafka_port).client


    # send one file to kafka
    def send_file_json(self, file_dict:dict, topic:str):
        try:
            self.producer.send(topic=topic, value=file_dict)

            logging.info(f'file: {file_dict} successfully send.')

        except Exception as e:
            logging.critical(f'failed to send file: {file_dict} to kafka, exception: {e}.')


    # return all the files within a given directory
    @staticmethod
    def files_within_dir(directory:str):
        try:
            path = Path(directory)
            files = [item for item in path.iterdir() if item.is_file()]
            return files

        except Exception as e:
            logging.critical(f'failed to get the list of files in directory: "{directory}", exception: {e}')


    # main function
    def run(self, files_dir_path:str, batches:int, send_topic:str):
        try:
            logging.info(f'getting all files from dir: "{files_dir_path}"')

            batch = batches
            temp_msg_send = 0
            sum_sent = 0

            files_iter = Path(files_dir_path).iterdir()
            for file in files_iter:

                if file.is_file():

                    file_dict = FileMetaMade.file_to_json(file_path=file)

                    logging.info(f'sending file metadata: {file_dict}')
                    self.send_file_json(file_dict=file_dict, topic=send_topic)

                    temp_msg_send += 1
                    sum_sent += 1

                    if temp_msg_send == batch:
                        temp_msg_send = 0
                        logging.info(f'send {temp_msg_send} - wait 3 sec.')
                        time.sleep(3)

            logging.info(f'finish to send files data - sent: {sum_sent}.')


        except Exception as e:
            logging.critical(f'failed occurred on manager.run, exception: {e}')


