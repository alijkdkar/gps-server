import base64
from datetime import time,datetime
import json
from typing import Hashable, List
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
        self.iconUrl :str=""
    
    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)
     
class CarServiceDetailVM :
    def __init__(self):
        self.sdId :int = 0
        self.serviceId :int = 0
        self.seviceName: str = ""
        self.ProductId :int = 0
        self.DateTime : DateTime 
        self.updateTime : DateTime 
        self.IsDeleted :Boolean=False
        self.maxValue :int = 0
        self.value :int =0
        self.periodCounter: int =0
        self.iconUrl :str=""
    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)



class WrongAreaVM:
    def __init__(self):
        self.ID : int = 0
        self.productID : int=0
        self.AreaName : str = ""
        self.DateTime : str = ""
        self.updateTime : str = ""
        self.IsDeleted : int = 0 
        self.details =[]
    
    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
                sort_keys=True, indent=4)

class WrongAreaDetail:
    def __init__(self) -> None:
        self.wdid :int=0
        self.wrongAreaID : int=0
        self.Longitude
        self.latitude

    def toJson(self):
         return json.dumps(self, default=lambda o: o.__dict__, 
                sort_keys=True, indent=4)
        