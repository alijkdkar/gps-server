import json
from typing import Type


class product():
    def __init__(self,pid,pname,pownerMobile,pOwnerPID,pMobile,ptype,pimage,mimiSerial,pCreattionDate,pUpdateDate,installerCode) -> None:
        self.pid = pid
        self.pname =str(pname or "")
        self.pOwnerPID = pOwnerPID
        self.pownerMobile = pownerMobile
        self.pMobile = pMobile
        self.ptype = ptype
        self.pimage = pimage
        self.mimiSerial = mimiSerial
        self.pcreateDate = pCreattionDate
        self.pUpdateDate = pUpdateDate
        self.installerCode = installerCode
        self.locations = "BBLLoCEDA"
    
    @property
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=False,ensure_ascii= False, indent=0) 
    

class locpoint():
    def __init__(self,lhid,ProductID,AddressName,DateTime,Longitude,latitude) -> None:
        self.lhid=lhid
        self.ProductID=ProductID
        self.AddressName =AddressName
        self.DateTime = DateTime
        #self.IsDeleted =IsDeleted
        self.Longitude =Longitude
        self.latitude=latitude

    @property
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=False,ensure_ascii= False, indent=0) 
    