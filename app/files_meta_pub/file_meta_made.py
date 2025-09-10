import pathlib
from datetime import datetime
from logger import Logger

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
                                      'created_time': str(datetime.fromtimestamp(stats.st_ctime)),
                                      'risk_rank': "unprocessed"}
                         }

            return file_dict

        except Exception as e:
            logger.error(f'exception occurred to jsonify file: {file_path}, exception: {e}.')



