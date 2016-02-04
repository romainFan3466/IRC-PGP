

from app.handlers.pgpHandler import PgpHandler
from simplejson import JSONEncoder
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES
from Crypto import Random

class Message:

    plaintext = ""
    signature = ""
    publicKey = ""

    def __init__(self, plaintext, publicKey=""):
        self.plaintext = plaintext
        self.publicKey = publicKey


    def sign(self, privateKey):
        self.signature = PgpHandler.sign(privateKey, self.plaintext)


    def verify(self):
        return PgpHandler.verify(self.plaintext, self.publicKey,self.signature)


    def __JSONencode(self):
        return JSONEncoder().encode(self.__dict__)

    def __getEncrypt(self):
        encoded = self.__JSONencode()
        password = PgpHandler.generateKey(32)
        key = PgpHandler.generateHash(password)
        return {
            "cipher" : PgpHandler.AESencrypt(self.plaintext, key),
            "AESkey" : password,
            "receiver_username" : "receiver" # at the final with rsa :
        }

    def getFinal(self):
        encrypted = self.__getEncrypt()
        return JSONEncoder().encode(encrypted)


    @staticmethod
    def rawParse(encodedMessage:str=""):
        pt = {}
        if "PRIVMSG" in encodedMessage:
            raw_user, type, target, raw_message = encodedMessage.split(sep=" ",maxsplit=3)
            user = raw_user[1:]
            user = user.split(sep="!")[0]
            message = raw_message[1:]
            pt["username"] = '<span style="color:blue; font-weight: bolder;">' + user + "</span>"
            pt["target"] = target
            pt["message"] = message
        return pt

    @staticmethod
    def exportNames(message, pattern):
        names = []
        names = message.split(sep=pattern)
        return names[1].split(sep=" ")