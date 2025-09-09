from gridfs import GridFS
from pymongo import MongoClient
from app.consume_and_persist.logger import Logger

logger = Logger.get_logger()

class MongoCRUD:
    def __init__(self, mdb_client:MongoClient):
        self.client = mdb_client

    # insert one document to mongo
    def insert_one(self, db_name:str, collection:str, doc:dict):
        try:

            collection = self.client[db_name][collection]
            result = collection.insert_one(doc)

            logger.info(f'doc: {doc} successfully inserted to mdb.')

            return str(result.inserted_id)

        except Exception as e:
            logger.error(f'exception occurred to insert doc: {doc}, exception: {e}')

    # saving a audio content to mdb
    def save_audio_content_file_on_mdb(self, db_name:str, collection_name:str, custom_id: str, audio_file_path: str, file_name:str):
        try:

            db = self.client[db_name]
            fs = GridFS(db, collection=collection_name)

            with open(audio_file_path, 'rb') as audio_file:
                file_id = fs.put(audio_file, _id=custom_id, filename=file_name)

            logger.info(f'successfully saved - {audio_file_path} - file content to mongo.')

            return file_id

        except Exception as e:
            logger.error(f'failed to saving file content of - {audio_file_path} - file to mongo, exception: {e}')

    # get one document by id
    def get_by_id(self, db_name:str, collection:str, id_: str):
        try:

            collection = self.client[db_name][collection]
            doc_found = collection.find_one({"_id": id_})

            return doc_found

        except Exception as e:
            logger.error(f'exception occurred to find doc id: {id_}, exception: {e}')

    # get all documents from mongo
    def find_all(self, db_name:str, collection:str):
        try:
            collection = self.client[db_name][collection]
            all_docs = collection.find().to_list

            return all_docs

        except Exception as e:
            logger.error(f'exception occurred to extract all documents from mongo, exception: {e}')

    # update one document by id
    def update_by_id(self, db_name:str, collection:str, id_: str, update_fields:dict):
        try:
            collection = self.client[db_name][collection]
            result = collection.update_one({"_id": id_}, {"$set": update_fields})

            logger.info(f'successfully updated document id: {id_}, result:{result}')

        except Exception as e:
            logger.error(f'exception occurred to update document id: {id_}, exception: {e}')

    # delete one document by id
    def delete_by_id(self, db_name:str, collection:str, id_:str):
        try:
            collection = self.client[db_name][collection]
            result = collection.delete_one({"_id": id_})

            logger.info(f'successfully delete id: {id_}, result:{result}')

        except Exception as e:
            logger.error(f'exception occurred to delete document id: {id_}, exception: {e}')