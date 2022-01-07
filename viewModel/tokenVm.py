import base64
from datetime import time,datetime
import json
from typing import Hashable
from hashlab import AESCipher
from flask.json import jsonify
from flask_cors.core import serialize_option
import constes

class Token:
    def __init__(self,Display,IsVakidated,id,userName):
        self.Display = Display
        self.isAuth = IsVakidated
        self.id = id
        self.userName = userName
        self.CreationDate =str(datetime.now())

    def __init__(self,jsonData):
        j = json.loads(jsonData)
        self.userName=j['userName']
        self.id = j['id']
        self.Display = j['Display']
        self.isAuth = j['IsVakidated']
        self.CreationDate =str( datetime.now())


    @property
    def tokenString(self):
        header =str(base64.encodestring( bytes("{alg: RS256,typ: JWT}".encode())).decode()).strip("\n")
        PayLoad=str(base64.encodestring(bytes( str(self.toJSON()).encode())).decode()).strip("\n")
        signiture =str( AESCipher(constes.CryptionKey).encrypt(header+"."+PayLoad).decode()).strip("\n")
        return header.strip("\n")+"."+PayLoad.strip("\n")+"."+signiture.strip("\n")

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)
    
    def checkToken(token):
        
        header,pyload,signiture = str(token).split('.')
        nowSignuture =str( AESCipher(constes.CryptionKey).encrypt(header+"."+pyload))
        if nowSignuture.replace('+',' ') == signiture:
            return True
        return False