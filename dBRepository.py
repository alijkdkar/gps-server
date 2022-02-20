from math import fabs
from re import X
from unicodedata import name
from matplotlib.style import use
import numpy as np
import pyodbc 
import pandas as pd
from  viewModel.productsVM import product as proc

from viewModel.mViewModels import Settingg
from viewModel.userVM import User
from viewModel.tokenVm import Token



# connection to db
class dbEntity:
    def __init__(self):
        self.server = '.\SQLEXPRESS2019' 
        self.database = 'gpsManager' 
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
        
        insertedID =  userp.saveDB(dbEntity = self)   
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
        """Modify product create and update"""
        try:
            query1 = "exec [pro].[uspModifyProduct] '{product}'".format(product=product.toJSON)
            self.cursor.execute(query1)
            self.cursor.commit()
        except Exception as X:
            print(X)
            return False
        
        return True

    def getProductBy(self,pid=None,pname=None):
        """ for get information about prodoucts by id that you must now :))"""
        if pid !=None:
            qury = f"select pid,pname,pOwnerMobile,pOwnerPID,pMobile,ptype,pimage,mimiSerial,pcreateDate,pUpdateDate,installerCode from pro.tblProducts where pid = {id}".format(id=pid)
        elif pname !=None:
            qury = f"select pid,pname,pOwnerMobile,pOwnerPID,pMobile,ptype,pimage,mimiSerial,pcreateDate,pUpdateDate,installerCode  from pro.tblProducts where pname like N'%{name}%'".format(name=pname)

        df =  pd.read_sql_query(qury,self.cnxn)

        res = [proc(r.pid,r.pname,r.pownerMobile,r.pOwnerPID,r.pMobile,r.ptype,r.pimage,r.mimiSerial,r.pCreattionDate,r.pUpdateDate,r.installerCode) for r in  df.iterrows()]
        return res
        
    
    def getProductsByOwner(self,ownerID):
        """get all Product of Online User that is avalable"""
        
        qury = "select pid,pname,pOwnerMobile,pOwnerPID,pMobile,ptype,pimage,mimiSerial,pcreateDate,pUpdateDate,installerCode from pro.tblProducts where pOwnerPID = {id}".format(id=ownerID)

        # df =  pd.read_sql_query(qury,self.cnxn)
        # for r in  df.iterrows():
        #     print(r)
        #res = [prod(r.pid,r.pname,r.pownerMobile,r.pOwnerPID,r.pMobile,r.ptype,r.pimage,r.mimiSerial,r.pCreattionDate,r.pUpdateDate,r.installerCode) for r in  df.iterrows()]
        res = []
        self.cursor.execute(qury) 
        row = self.cursor.fetchone() 
        while row: 
            p =  proc(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9],row[10])    
            res.append(p)
            
            row = self.cursor.fetchone()
            
        
        return res
