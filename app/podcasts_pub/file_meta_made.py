import json
import logging
from pathlib import Path

logging.basicConfig(level=logging.DEBUG,format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',handlers=[logging.FileHandler("file_meta_made.log"),logging.StreamHandler()])


class FileMetaMade:
    def __init__(self):
        pass


    # creating the metadata on the given file path
    @staticmethod
    def file_to_json(file_path:str):
        try:
            logging.info(f'jsonify file: {file_path}')

            path_obj = Path(file_path)
            stats = path_obj.stat()

            file_dict = {'absolute_path': path_obj.absolute(),
                         'type': path_obj.suffix,
                         'name': path_obj.name,
                         'size_in_megabytes': stats.st_size / 1000000,
                         'created_time': stats.st_ctime}

            return file_dict

        except Exception as e:
            logging.critical(f'exception occurred to jsonify file: {file_path}, exception: {e}.')



