import random as randm
from cryptography.fernet import Fernet

def createvalidationCode():
  return randm.randint(100000,999999)

global cipher_suite 
cipher_suite = None

def getHasherInstance(cipher):
  
   if cipher is None:
      key  = Fernet.generate_key()
      cipher_suite = Fernet(key)
      return cipher_suite
   else:
      return cipher

def encriptText(txt):
  
 
  encoded_text = cipher_suite.encrypt(txt)
  return encoded_text

def encriptText(hashtxt):
  key = Fernet.generate_key() #this is your "password"
  cipher_suite = Fernet(key)
  decoded_text = cipher_suite.decrypt(hashtxt)
  return decoded_text


def createToken(user):
  return ""


def sendSms(phonNum,txt):
    
    if phonNum == "0":
        return 'no number Recive themcall'
    else:
        return phonNum+' themcall'