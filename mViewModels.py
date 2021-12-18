import base64
from datetime import time,datetime
import json
from typing import Hashable
from hashlab import AESCipher
from flask.json import jsonify
from flask_cors.core import serialize_option


class Settingg:
    def __init__(self,settingId,Name,value,Desc,systemID) -> None:
        self.settingIDd = settingId
        self.name = Name
        self.value = value
        self.Desc = Desc
        self.systemId = systemID
    
    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)

class User:
    def __init__(self,userName,password,name,lastName):
     self.userName = userName,
     self.password=password,
     self.name =name,
     self.lastName = lastName
     

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
        header =str(base64.encodestring( bytes("{alg: RS256,typ: JWT}".encode())))
        print("Step 1==>"+header)
        PayLoad=str(base64.encodestring(bytes( str(self.toJSON()).encode())))
        signiture =str( AESCipher("662ede816988e58fb6d057d9d85605e0").encrypt(header+"."+PayLoad))
        return header+"."+PayLoad+"."+signiture

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)