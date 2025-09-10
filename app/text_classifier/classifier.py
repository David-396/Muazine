import re
from logger import Logger

logger = Logger().get_logger()

class Classifier:
    def __init__(self, hostile_list:list, less_hostile_list:list, percent_is_bds_threshold:float, risk_binds:list[float]):
        self.hostile_list = hostile_list
        self.less_hostile_list = less_hostile_list
        self.percent_is_bds_threshold = percent_is_bds_threshold
        self.risk_binds = risk_binds
        # print('HOSTILE_LIST:', self.hostile_list, 'LESS_HOSTILE_LIST:', self.less_hostile_list)


    @staticmethod
    def highlighted_words(text: str):
        try:

            if not text:
                return None

            words_detected = []
            for word in text:
                matches_words = re.findall(r"<em>(.*?)</em>", word)
                words_detected += matches_words
                # print('WORD:',word, 'WORDS_DETECTED:',words_detected)

            return words_detected

        except Exception as e:
            logger.error(f'failed to extract the highlighted words from text: {text}, exception: {e}')

    # calculating the hostile percent
    def bds_percent(self, result_doc:dict):
        try:
            if "highlight" not in result_doc:
                return result_doc['_score'] * 100

            # get the score of the doc - to see how much the hostile and not hostile words are match to the lists
            score = result_doc['_score']
            # getting all the matches words that found in the text - hostile and less hostile
            matches_words = self.highlighted_words(text=result_doc['highlight']['metadata.recognized_text'])

            # mapping them by hostile and not
            mapping_dict = {'hostile':[], 'less_hostile':[]}

            for word in matches_words:
                word = word.lower()
                if word in self.hostile_list:
                    mapping_dict['hostile'].append(word)

                elif word in self.less_hostile_list:
                    mapping_dict['less_hostile'].append(word)

            # get the len of all the text
            all_text_len = len(result_doc['_source']['metadata']['recognized_text'].split(' '))
            # calculate how much its hostile:
            #       calculate the ratio between the matched words to all the text and double it - because its the hostile percent
            percent_hostile = (len(mapping_dict['hostile']) / all_text_len) * 2

            # calculate how much its less hostile:
            #       calculate the ratio between the matched words to all the text
            percent_less_hostile = len(mapping_dict['less_hostile']) / all_text_len

            # adding them and double in score - in case that the recognized hostile words weren't exactly as listed in the hostile words list,
            # but were a little distorted.
            # so if it were distorted it will lower the percent , and if not it will increase the percent.
            sum_percent = (percent_hostile + percent_less_hostile) * score * 100

            # print('SCORE:', score, 'PERCENT_HOSTILE:',percent_hostile, 'PERCENT_LESS_HOSTILE:',percent_less_hostile, 'SUM_PERCENT:',sum_percent, 'MATCHES_WORDS:',matches_words, 'MAPPING_DICT:',mapping_dict)

            return sum_percent

        except Exception as e:
            logger.error(f'failed to calculate the bds percent, exception: {e}')

    # true if the percent bigger than the threshold else false
    def is_bds(self, percent:float):
        try:
            if percent is None:
                return False

            return percent >= self.percent_is_bds_threshold

        except Exception as e:
            logger.error(f'failed to calculate the is_bds boolean, exception: {e}')

    # return the risk rank by the binds list
    def risk_rank(self, percent:float):
        try:
            risk = 'NONE'

            if percent is None:
                return risk

            if percent >= self.risk_binds[0]:
                risk = 'MEDIUM'
            if percent >= self.risk_binds[1]:
                risk = 'HIGH'

            return risk
        except Exception as e:
            logger.error(f'failed to calculate the risk rank, exception: {e}')
