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
    
    @property
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=False,ensure_ascii= False, indent=0) 