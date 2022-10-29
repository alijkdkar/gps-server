from typing_extensions import Self
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
import json


db = SQLAlchemy()

class User(db.Model):
    id = db.Column('User_id', db.Integer, primary_key = True)
    personelID = db.Column(db.Integer)
    userName = db.Column(db.String(100))
    password = db.Column(db.String(1000))
    name = db.Column(db.String(100))
    lastName = db.Column(db.String(100))
    createdDateTime = db.Column(db.DateTime(timezone=True),server_default=func.now())
    email = db.Column(db.String(100))
    

    def __init__(self,userName=None,password="",name=None,lastName=None,createdDateTime=None,email=None,personelID=None,id=None):
        self.id = id or 0  ,
        self.personelID = personelID,
        self.userName = userName,
        self.password: str =password,
        self.name =name,
        self.lastName = lastName,
        self.createdDateTime = createdDateTime,
        self.email = email
    
class product(db.Model):
    pid = db.Column('product_id' , db.Integer , primary_key = True)
    pname = db.Column(db.String(100))
    pOwnerPID = db.Column(db.Integer)
    pownerMobile = db.Column(db.String(15))
    pMobile = db.Column(db.String(15))
    ptype = db.Column(db.Integer)
    pimage = 
    

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
    