from re import X
import pyodbc 
import pandas as pd

from viewModel.mViewModels import Settingg
from viewModel.userVM import User


# connection to db
class dbEntity:
    def __init__(self):
        self.server = '.\SQLEXPRESS2014' 
        self.database = 'gpsDB' 
        self.username = 'sa' 
        self.password = '123456789' 
        self.cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER='+self.server+';DATABASE='+self.database+';UID='+self.username+';PWD='+ self.password)
        self.cursor = self.cnxn.cursor()


    def getSetting(self,customerID):
        #self.cursor.execute('select * from settings')
        if customerID is None:
            df = pd.read_sql_query("select * from settings",self.cnxn)
        else:
            df = pd.read_sql_query("select * from settings where customerID ="+str( customerID),self.cnxn)


        listofSetting= [(Settingg(row.id,row.name,row.value,row.Description)) for index, row in df.iterrows() ]  

        return listofSetting
    

    
    def signUpMember(self,userp):
        
        # username = userp.userName[0]
        # name = userp.name[0] or 'unname'
        # lastName = userp.lastName[0] or 'unlastname'
        # displayName=name+' '+lastName
        insertedID =  userp.saveDB(cursor = self.cursor)
        
        # query = """if not exists (select 1 from sec.users where userName='{usernamearg}' )
        #            insert into sec.personel([Name],[LastName],[DisplayName]) values ('{namearg}','{LastNamearg}','{dsnamearg}')""".format(usernamearg=username,namearg=name,LastNamearg=lastName,dsnamearg=displayName)
        # print(query)
        
        # self.cursor.execute(query)
        # self.cursor.commit()
        #print(query)

        #todo : save Youser and Personel to DataBase
        
        
        return insertedID

    def SaveToken(self,PersonelID=0,token=""):
        try:
            query = "insert into sec.tokens ( userID, token) values ({personID},'{token}')".format(personID=PersonelID,token=str(token).replace("'",""))
            print(query)
            self.cursor.execute(query)
            self.cursor.commit()
        except Exception as X:
            print(X)
            return False
        
        return True