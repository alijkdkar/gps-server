import base64
from datetime import datetime
import json
from hashlab import AESCipher

import constes

class Token:
    def __init__ (self,Display="",IsValidated=False,id=0,userName=None,password=None):
        self.Display = Display
        self.isAuth = IsValidated
        self.id = id
        self.userName = userName
        self.CreationDate =str(datetime.now())
        self.password = password


    def fillByJson(self,jsonData):
        j = json.loads(jsonData)
        self.userName=j['userName']
        self.id = j['id']
        self.Display = j['Display']
        self.isAuth = j['IsVakidated']
        self.CreationDate =str( datetime.now())
        self.password = j['password']
        return self
    
    @property
    def tokenString(self):
        header =str(base64.encodebytes( bytes("{alg: RS256,typ: JWT}".encode())).decode()).replace('\n','').replace('\\n','')
        PayLoad=str(base64.encodebytes(bytes( str(self.toJSON()).encode())).decode()).replace('\n','').replace('\\n','')
        signiture =str(base64.encodebytes( AESCipher(constes.CryptionKey).encrypt(header+"."+PayLoad)).decode()).replace('\n','').replace('\\n','')
        return header.replace('\n','').replace('\\n','')+"."+PayLoad.replace('\n','').replace('\\n','')+"."+signiture.replace('\n','').replace('\\n','')

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)
    
    
    def checkToken(token):
        header,pyload,signiture = str(token).split('.')
        nowSignuture =str(base64.encodebytes( AESCipher(constes.CryptionKey).encrypt(header+"."+pyload)).decode()).strip("\n").replace('\n','').replace('\\n','')
        if nowSignuture ==  signiture.replace('\n','').replace('\\n',''):
            
            return True
        return False

    def create_new_token():
        return Token("behzad bluekian",True,0,"alijkdkar","2120")
    
    def create_new_HashToken():
        return Token("behzad bluekian",True,0,"alijkdkar","2120").tokenString

    def create(self,token):
        
        header,pyload,signiture = str(token).split('.')
        
        dd =base64.b64decode(pyload).decode()
            
        j = json.loads(dd)
        self.userName=j['userName']
        self.id = j['id']
        self.Display = j['Display']
        self.isAuth = j['isAuth']
        self.CreationDate = j['CreationDate']
        #self.password = j['password']
        return self
        
    