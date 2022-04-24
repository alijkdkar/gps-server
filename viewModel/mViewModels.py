import base64
from datetime import time,datetime
import json
from typing import Hashable
from xmlrpc.client import Boolean, DateTime
from hashlab import AESCipher
from flask.json import jsonify
from flask_cors.core import serialize_option
import constes

class Settingg:
    def __init__(self,settingId,Name,value,Desc,systemID='111') -> None:
        self.settingIDd = settingId
        self.name = Name
        self.value = value
        self.Desc = Desc
        self.systemId = systemID
    
    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)



class CarService:
    def __init__(self):
        self.servid :int=0
        self.serviceName :str=""
        self.DateTime :datetime 
        self.updateTime :datetime
        self.IsDeleted :Boolean = False
        self.isSystem :Boolean =True
    
    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)
     
class CarServiceDetailVM :
    def __init__(self):
        self.sdId :int = 0
        self.serviceId :int = 0
        self.ProductId :int = 0
        self.DateTime : DateTime 
        self.updateTime : DateTime 
        self.IsDeleted :Boolean=False
        self.maxValue :int = 0
        self.value :int =0
        self.periodCounter: int =0