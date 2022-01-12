# class HashLaber(type):
import base64
import hashlib
from Crypto import Random
from Crypto.Cipher import AES

class AESCipher(object):


    def __init__(self, key): 
        self.bs = AES.block_size
        self.key = key.encode()

    def encrypt(self, raw):
        raw = self._pad(raw)
        #iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_ECB)
        return base64.b64encode( cipher.encrypt(raw.encode()))

    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        #iv = enc[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_ECB)
        return self._unpad(cipher.decrypt(enc)).decode('utf-8')

    def _pad(self, s):
        return s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)

    @staticmethod
    def _unpad(s):
        return s[:-ord(s[len(s)-1:])]

    