import hashlib


class Hash:
    def __init__(self):
        pass

    def hash(self, string:str):

        encoded_string = string.encode('utf-8')
        return int(hashlib.sha256(encoded_string).hexdigest(), 16)

        

# print(str(Hash().hash('hello')))
# print(int(hashlib.sha256(encoded_string).hexdigest(), 16))
# sha256_hash = hashlib.sha256(encoded_string).hexdigest()
# # print(hash('hello'))