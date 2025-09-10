import os
from base64_decrypt import decrypt_from_base64
from manager import Manager
from logger import Logger

logger = Logger().get_logger()

ES_HOST = os.getenv('ES_HOST')
ES_PORT = os.getenv('ES_PORT')
ES_INDEX = os.getenv('ES_INDEX')

HOSTILE_ENCRYPT_TEXT = os.getenv('HOSTILE_ENCRYPT_TEXT')
LESS_HOSTILE_ENCRYPT_TEXT = os.getenv('LESS_HOSTILE_ENCRYPT_TEXT')
PERCENT_IS_BDS_THRESHOLD = float(os.getenv('PERCENT_IS_BDS_THRESHOLD'))
RISK_BINDS = [40,80]

logger.info('init the classifier manager...')

manager = Manager(es_host=ES_HOST,
                  es_port=ES_PORT,
                  es_index=ES_INDEX,
                  hostile_lst=decrypt_from_base64(HOSTILE_ENCRYPT_TEXT).lower().split(','),
                  less_hostile_lst=decrypt_from_base64(LESS_HOSTILE_ENCRYPT_TEXT).lower().split(','),
                  percent_is_bds_threshold=PERCENT_IS_BDS_THRESHOLD,
                  risk_binds=RISK_BINDS
                  )

logger.info('running the classifier..')

manager.run_classifier()