import speech_recognition as sr
import logger

logger = logger.Logger().get_logger()

class Stt:
    def __init__(self):
        self.recognizer = sr.Recognizer()


    def recognize(self, file_path:str):
        try:

            with sr.AudioFile(file_path) as source:
                audio = self.recognizer.record(source)
                text = self.recognizer.recognize_google(audio)

                logger.info(f'text for file {file_path} successfully recognized.')

                return text

        except Exception as e:
            logger.error(f'failed to convert audio to text in {file_path}, exception: {e}')

