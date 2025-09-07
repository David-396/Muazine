import logging
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

            logging.info(f'file: "{file_dict['name']}" successfully send.')

        except Exception as e:
            logging.critical(f'failed to send file: "{file_dict['name']}" to kafka, exception: {e}.')


    # return all the files within a given directory
    @staticmethod
    def files_within_dir(directory:str):
        try:
            path = Path(directory)
            files = [item for item in path.iterdir() if item.is_file()]
            return files

        except Exception as e:
            logging.critical(f'failed to get the list of files in directory: "{directory}", exception: {e}')


    # # main function
    # def run(self, files_dir_path:str):
    #     try:
    #         logging.info(f'getting all files from dir: "{files_dir_path}"')
    #         files_to_send = self.files_within_dir(directory=files_dir_path)
    #
    #         batch = 10
    #
    #         while files_to_send:
    #
    #             for file in files_to_send:
    #                 file_path =
    #                 file_dict = FileMetaMade.file_to_json(file_path=file_path)

        #
        #
        #
        #
        # except Exception as e:
        #     logging.critical(f'failed occurred on manager.run, exception: {e}')


