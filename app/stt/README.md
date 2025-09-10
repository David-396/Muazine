STT:
    
    the service is convert an audio file to text with speech_to_text package.
    the stt consume from kafka the json file metadata and add a column of recognized_text with the recognized text.
    
    the stt doesnt read from elastic and make the update there because there is not any meaning to the json if the text doesnt exist in the json
    so the stt consume the json and send to the kafka the complete service.