from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func

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
    
