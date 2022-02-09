from math import fabs
from re import X
from matplotlib.style import use
import pyodbc 
import pandas as pd

from viewModel.mViewModels import Settingg
from viewModel.userVM import User
from viewModel.tokenVm import Token


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
        
        insertedID =  userp.saveDB(cursor = self.cursor)   
        return insertedID


    def signInWithPassword(self,username,password):
        
        user=User().GetUserFromDbByUserName(username= username)
        
        if user.password == password:
            token = Token(Display=user.userName,IsValidated=True,id =user.id,userName = user.userName,password = "" )
            
            self.SaveToken(user.personelID or user.personelID,token= token.tokenString)
            return user,token
        else:
            return None,None


    def SaveToken(self,PersonelID=0,token=""):
        try:
            query = "insert into sec.tokens ( userID, token) values ({personID},'{token}')".format(personID=PersonelID,token=str(token).replace("'",""))
            self.cursor.execute(query)
            self.cursor.commit()
        except Exception as X:
            print(X)
            return False
        
        return True

    def saveProduct(self,product):
        try:
            query = "prs.uspModifyProduct {id},{product}".format(id=product.pid,product=product.toJSON)
            self.cursor.execute(query)
            self.cursor.commit()
        except Exception as X:
            print(X)
            return False
        
        return True

    def getProductById(self):
        pass
    
    def getProductsByOwner(self):
        pass
