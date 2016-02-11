from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES
from Crypto import Random
from app import config
import base64, random, string

#TODO : handle Message instence instead of str, bytes, long

BS = 16
pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
unpad = lambda s : s[:-ord(s[len(s)-1:])]

class PgpHandler:


    @staticmethod
    def exportKey(key):
        return key.exportKey("PEM")


    @staticmethod
    def sign(key, text:str):
        if isinstance(key, str):
            key = RSA.importKey(key)
        hash = SHA256.new(text.encode()).digest()
        return key.sign(hash, '')


    @staticmethod
    def RSAencrypt(key, text:str):
        if isinstance(key, str):
            key = RSA.importKey(key)
        return base64.b64encode(key.encrypt(text.encode(),32)[0])


    @staticmethod
    def RSAdecrypt(key, encrypted:bytes):
        if isinstance(key, str):
            key = RSA.importKey(key)
        return key.decrypt(base64.b64decode(encrypted)).decode()


    @staticmethod
    def verify(plaintext, publicKey, signature):
        hash = SHA256.new(plaintext.encode()).digest()
        return publicKey.verify(hash, signature)


    @staticmethod
    def generateNewPairs():
        random_generator = Random.new().read
        generation = RSA.generate(config["RSA_KEY_LENGTH"], random_generator)
        return {"private" : generation, "public" : generation.publickey()}


    @staticmethod
    def generateHash(key:str):
        return  SHA256.new(key.encode()).digest()


    @staticmethod
    def generateKey(length):
        return ''.join([random.choice(string.ascii_letters + string.digits) for n in range(32)])

    @staticmethod
    def AESencrypt(plaintext, key):
        plaintext = pad(plaintext)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(plaintext))


    @staticmethod
    def AESdecrypt(enc, key):
        enc = base64.b64decode(enc)
        iv = enc[:16]
        cipher = AES.new(key, AES.MODE_CBC, iv)
        ret = unpad(cipher.decrypt(enc[16:]))
        return ret.decode()
