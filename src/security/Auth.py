import jwt
from decouple import config
import string
import random

class Auth:
    def decodeToken(self, token):
        return jwt.decode(token, self.__getSecretKey(),algorithms=['HS256'])

    def generateToken(self, data):
        key = self.__getSecretKey()
        return jwt.encode(data,key,algorithm="HS256")

    def __getSecretKey(self):
        return config('SECRETKEY')

    def generate_secret_key(self):
        random_str = string.ascii_letters + string.digits + string.ascii_uppercase
        secret_key = ''.join(random.choice(random_str) for i in range(256))
        print(secret_key)

