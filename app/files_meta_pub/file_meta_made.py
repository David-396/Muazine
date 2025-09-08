import logging
import pathlib
from datetime import datetime
from app.logger import Logger

logging.basicConfig(level=logging.INFO,format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',handlers=[logging.FileHandler("files_meta_pub.log"),logging.StreamHandler()])

logger = Logger.get_logger()

class FileMetaMade:
    def __init__(self):
        pass


    # creating the metadata on the given file path
    @staticmethod
    def file_to_json(file_path:pathlib.Path):
        try:

            stats = file_path.stat()

            file_dict = {'absolute_path': str(file_path.absolute()),
                         'metadata': {'type': file_path.suffix,
                                     'name': file_path.name,
                                     'size_in_megabytes': stats.st_size / 1000000,
                                     'created_time': str(datetime.fromtimestamp(stats.st_ctime))}
                         }

            return file_dict

        except Exception as e:
            logging.critical(f'exception occurred to jsonify file: {file_path}, exception: {e}.')
            logger.error(f'exception occurred to jsonify file: {file_path}, exception: {e}.')



