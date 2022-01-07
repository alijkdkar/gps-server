
import pandas as pd
import dBRepository as db

class User:
    

    def __init__(self,userName=None,password=None,name=None,lastName=None,createdDateTime=None,email=None,personelID=None,id=None):
        self.id = id or 0  ,
        self.personelID = personelID,
        self.userName = userName,
        self.password=password,
        self.name =name,
        self.lastName = lastName,
        self.createdDateTime = createdDateTime,
        self.email = email
    



    def GetUserFromDbByUserName(self,username):
        cnxcc = db.dbEntity().cnxn
        data = pd.read_sql_query("""select * from sec.[users]  as u join sec.personel as p on u.personelID = p.id where userName = '{username}' """.format(username = int(username)),cnxcc)
        for index,row in data.iterrows():
            self.id = row.id
            self.personelID = row.personelID
            self.userName = row.userName
            self.name = row.Name
            
        
        return self
    
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