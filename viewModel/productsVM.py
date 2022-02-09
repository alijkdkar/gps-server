import json


class product():
    def __init__(self,pid,pname,pownerMobile,pMobile,ptype,pimage,mimiSerial,pCreattionDate,pUpdateDate,installerCode) -> None:
        self.pid = pid
        self.pname =pname
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
            sort_keys=False, indent=0) 