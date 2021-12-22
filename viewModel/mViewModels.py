import base64
from datetime import time,datetime
import json
from typing import Hashable
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


     
