from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto import Random

#TODO : handle Message instence instead of str, bytes, long

class PgpHandler:

    RSAkey = None
    keyLength = 2048


    def __init__(self):
        self.generateNewPairs()


    def getPublicKey(self):
        return self.RSAkey.publickey().exportKey("PEM")


    def sign(self, text:str):
        hash = SHA256.new(text.encode()).digest()
        return self.RSAkey.sign(hash, '')


    def encrypt(self, text:str):
       return self.RSAkey.publickey().encrypt(text.encode(),32)


    def decrypt(self, encrypted:bytes):
        return self.RSAkey.decrypt(encrypted).decode()


    def verify(self, encrypted, publicKey):
        return publicKey.verify(encrypted, publicKey)

    def generateNewPairs(self):
        random_generator = Random.new().read
        self.RSAkey= RSA.generate(self.keyLength, random_generator)