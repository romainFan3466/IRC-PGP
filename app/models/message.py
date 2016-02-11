

from app.handlers.pgpHandler import PgpHandler
from simplejson import JSONEncoder, JSONDecoder, JSONDecodeError
import base64, zlib

class Message:

    plaintext = ""
    signature = ""
    publicKey = ""

    def __init__(self, plaintext, publicKey):
        self.plaintext = plaintext
        self.publicKey = publicKey


    def __JSONencode(self):
        return JSONEncoder(separators=(',', ':')).encode(self.__dict__)


    def __getCipherText(self):
        # AES encrypt
        password = PgpHandler.generateKey(32)
        key = PgpHandler.generateHash(password)
        cipher = PgpHandler.AESencrypt(self.plaintext, key)
        # cipher = base64.b64encode(zlib.compress(cipher,9))
        return {
            "cipher" : cipher,
            "AESkey" : password,
        }

    def getFinal(self, receiver):
        encrypted = self.__getCipherText()
        # encrypted = JSONEncoder().encode(encrypted)
        encryptedRSA = PgpHandler.RSAencrypt(self.publicKey, encrypted["AESkey"])
        obj = {
            "to" : receiver,
            "cipher" :  encrypted["cipher"],
            "AESEncryptedKey" : encryptedRSA
        }
        return JSONEncoder(separators=(',', ':')).encode(obj)


    def getPlainText(self):
        return self.plaintext


    @staticmethod
    def decrypt(encrypted, privateKey):

            try :
                encrypted = JSONDecoder().decode(encrypted)
                if "cipher" in encrypted and "AESEncryptedKey" in encrypted:
                    AESkey= PgpHandler.RSAdecrypt(privateKey,encrypted["AESEncryptedKey"])
                    AESkey = PgpHandler.generateHash(AESkey)
                    plaintext = PgpHandler.AESdecrypt(encrypted["cipher"], AESkey)
                    return Message(plaintext,"")
                return None
            except Exception as e:
                print(e)
                pass


    @staticmethod
    def rawParse(encodedMessage:str=""):
        pt = {}
        raw_user, type, target, raw_message = encodedMessage.split(sep=" ",maxsplit=3)
        user = raw_user[1:]
        user = user.split(sep="!")[0]
        message = raw_message[1:]
        pt["username"] = '<span style="color:blue; font-weight: bolder;">' + user + "</span>"
        pt["target"] = target
        pt["message"] = message
        return pt



    @staticmethod
    def decode(encoded):
        try :
           obj = JSONDecoder().decode(encoded)
        except JSONDecodeError:
            return None
        else:
            return obj


    @staticmethod
    def exportNames(message, pattern):
        names = []
        names = message.split(sep=pattern)
        return names[1].split(sep=" ")