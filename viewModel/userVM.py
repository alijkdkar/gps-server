

class User:
    def __init__(self,userName,password,name,lastName,createdDateTime,email,personelID,id=None):
     self.id = id or 0  ,
     self.personelID = personelID,
     self.userName = userName,
     self.password=password,
     self.name =name,
     self.lastName = lastName,
     self.createdDateTime = createdDateTime,
     self.email = email
     
    def __init__(self):
        self=  self