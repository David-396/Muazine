import json
import logging
import pathlib
from pathlib import Path

logging.basicConfig(level=logging.DEBUG,format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',handlers=[logging.FileHandler("file_meta_made.log"),logging.StreamHandler()])


class FileMetaMade:
    def __init__(self):
        pass


    # creating the metadata on the given file path
    @staticmethod
    def file_to_json(file_path:pathlib.Path):
        try:
            logging.info(f'jsonify file: {file_path.name}')

            stats = file_path.stat()

            file_dict = {'absolute_path': file_path.absolute(),
                         'metadata': {'type': file_path.suffix,
                                     'name': file_path.name,
                                     'size_in_megabytes': stats.st_size / 1000000,
                                     'created_time': stats.st_ctime}
                         }

            return file_dict

        except Exception as e:
            logging.critical(f'exception occurred to jsonify file: {file_path}, exception: {e}.')



