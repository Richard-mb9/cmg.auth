import jwt
from src.utils.getEnv import getEnv

class Auth:
    def decodeToken(self, token):
        return jwt.decode(token, self.__getSecretKey(),algorithms=['HS256'])

    def generateToken(self, data):
        key = self.__getSecretKey()
        return jwt.encode(data,key,algorithm="HS256")

    def __getSecretKey(self):
        return getEnv('secretkey')


