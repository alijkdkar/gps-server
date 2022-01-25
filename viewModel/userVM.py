
from flask.json import jsonify
import pandas as pd
import dBRepository as db
import json
import datetime




class User:
    

    def __init__(self,userName=None,password="",name=None,lastName=None,createdDateTime=None,email=None,personelID=None,id=None):
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
        data = pd.read_sql_query("""select distinct u.id,u.personelID,u.userName,u.email,p.DisplayName,p.Name,u.[password] ,p.LastName,p.createdDateTime from sec.[users]  as u join sec.personel as p on u.personelID = p.id where userName = '{username}' """.format(username = int(username)),cnxcc)
        print(data)
        dt_string = "2020-12-18 3:11:09" 
        format = "%Y-%m-%d %H:%M:%S"
        # for index,row in data.iterrows():
        #     self.id = int (row.id[0])
        #     self.personelID = int (row.personelID)
        #     self.userName = str(row.userName)
        #     self.name = str(row.Name)
        #     #self.password=str(row.password or None),
        #     self.lastName = str(row.LastName[0] or None),
        #     #self.createdDateTime =int(datetime.datetime.strptime(row.createdDateTime[0], format)), #row.createdDateTime,
        #     self.email = str(row.email or None)
        
        df = pd.DataFrame(data, columns = ['id', 'personelID', 'userName','Name','password','LastName','createdDateTime','email'])
        print(df)
        print(str( df.iloc[0].createdDateTime)[0:19])

        self.id = int (df.iloc[0].id)
        self.personelID = int (df.iloc[0].personelID)
        self.userName = str(df.iloc[0].userName)
        self.name = str(df.iloc[0].Name)
        self.password=str(df.iloc[0].password),
        self.lastName = str(df.iloc[0].LastName),
        self.createdDateTime =str( datetime.datetime.strptime(str( df.iloc[0].createdDateTime)[0:19], format)), #df.iloc[0].createdDateTime,
        self.email = str(df.iloc[0].email or None)



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
                            ({personelID},{userName},{password},{email})""".format(personelID = id,userName=username,password =self.password,email=self.email or 'NULL')
            print(query)
            cursor.execute(query)
            # cursor.execute("SELECT @@IDENTITY AS ID;")
            # userid =  cursor.fetchone()[0]               
                           
        cursor.commit()
        
        print(id)
         
        return id

    @property
    def userJsonString(self):
        return self.toJSON().strip("\n")

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=False, indent=0)

        
    # def toJSON(self):
    #     data = {
    #         'id':self.id or "" ,
    #         'personelID':self.personelID or "",
    #         'userName':self.userName or "",
    #         'password':self.password or "",
    #         'name':self.name or "",
    #         'lastName':self.lastName or "",
    #         'createdDateTime':self.createdDateTime or "",
    #         'email':self.email or ""
    #         }
    #     return jsonify(data)