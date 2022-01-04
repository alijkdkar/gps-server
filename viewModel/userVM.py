import pandas as pd

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

    
    def saveDB(self,cursor):
        username = self.userName[0]
        name = self.name[0] or 'unname'
        lastName = self.lastName[0] or 'unlastname'
        displayName=name+' '+lastName
        query = """set nocount on; if not exists (select 1 from sec.users where userName='{usernamearg}' ) 
                            insert into sec.personel([Name],[LastName],[DisplayName]) 
                            values ('{namearg}','{LastNamearg}','{dsnamearg}')""".format(usernamearg=int(username) ,namearg=name,LastNamearg=lastName,dsnamearg=displayName)
        print(query)
        cursor.execute(query)
        cursor.execute("SELECT @@IDENTITY AS ID;")
        id =  cursor.fetchone()[0]

        if id is not None or 0:
            query = """insert into sec.users(personelID,userName,[password],email) values
                            ({personelID},{userName},NULL,{email})""".format(personelID = id,userName=username,email=self.email or 'NULL')
            print(query)
            cursor.execute(query)
            # cursor.execute("SELECT @@IDENTITY AS ID;")
            # userid =  cursor.fetchone()[0]               
                           
        cursor.commit()
        
        print(id)
         
        return id