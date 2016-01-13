import app

#TODO : make the app runnable

from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto import Random

random_generator = Random.new().read

#### message to send ####
my_plain_text_message= "salut"

## private key ####
RSAkey = RSA.generate(2048, random_generator)

### public key export for sql ####
pubKey = RSAkey.publickey().exportKey("PEM")

###hash for signature
hash = SHA256.new(my_plain_text_message.encode()).digest()

signature = RSAkey.sign(hash, '')

enc =  RSAkey.publickey().encrypt(my_plain_text_message.encode(),32)

enc.verify

tex = RSAkey.decrypt(enc)
print(tex.decode())
#print(type(hash))
#
# signature = RSAkey.sign(hash, rng)
#
# RSAkey.verify(hash, signature)     # This sig will check out
# 1
# RSAkey.verify(hash[:-1], signature)# This sig will fail