from asyncio.windows_events import NULL
from datetime import datetime
from lib2to3.pgen2.token import EQUAL
from math import fabs
from re import X
from unicodedata import name
from xmlrpc.client import DateTime
from matplotlib.style import use
import numpy as np
import pyodbc 
import pandas as pd
from  viewModel.productsVM import locpoint, product as proc

from viewModel.mViewModels import Settingg, CarService, CarServiceDetailVM
from viewModel.userVM import User
from viewModel.tokenVm import Token
from dateutil.relativedelta import *


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
            query1 = "exec [pro].[uspModifyProduct] @jsonProductInput = N'{product}'".format(product=product.toJSON)
            self.cursor.execute(query1)
            self.cursor.commit()
        except Exception as X:
            print(X)
            return False
        
        return True

    def getProductBy(self,pid=None,pname=None):
        """ for get information about prodoucts by id that you must now :))"""
        if pid !=None:
            qury = f"select pid,pname,pOwnerMobile,pOwnerPID,pMobile,ptype,pimage,mimiSerial,pcreateDate,pUpdateDate,installerCode from pro.tblProducts as tp join sec.users as u on tp.pOwnerPID=u.personelID where u.id = {id}".format(id=pid)
        elif pname !=None:
            qury = f"select pid,pname,pOwnerMobile,pOwnerPID,pMobile,ptype,pimage,mimiSerial,pcreateDate,pUpdateDate,installerCode  from pro.tblProducts where pname like N'%{name}%'".format(name=pname)

        df =  pd.read_sql_query(qury,self.cnxn)

        res = [proc(r.pid,r.pname,r.pownerMobile,r.pOwnerPID,r.pMobile,r.ptype,r.pimage,r.mimiSerial,r.pCreattionDate,r.pUpdateDate,r.installerCode) for r in  df.iterrows()]
        return res
        
    
    def getProducts(self,ownerID,ProductID):
        """get all Product of Online User that is avalable"""
        if ProductID == 0 or ProductID == None:
            qury = "select pid,pname,pOwnerMobile,pOwnerPID,pMobile,ptype,pimage,mimiSerial,CAST( pcreateDate as smalldatetime),cast(pUpdateDate as smalldatetime),installerCode from pro.tblProducts as tp where tp.pOwnerPID = {ownerID}".format(ownerID=ownerID)
        elif ownerID != 0 and (ProductID != 0 or ProductID != None):
            qury = "select  pid,pname,pOwnerMobile,pOwnerPID,pMobile,ptype,pimage,mimiSerial,CAST( pcreateDate as smalldatetime),cast(pUpdateDate as smalldatetime),installerCode from pro.tblProducts as tp where tp.pOwnerPID = {ownerID} and tp.pid ={pid}".format(ownerID=ownerID,pid=ProductID)

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


    def getProductsHisLoc(self,ProductID=NULL,OwnerID=NULL,StartDateTime='',EndDateTime=datetime.now().strftime("%Y-%m-%d %H:%M:%S")):
        """get products location"""
        if StartDateTime == '':
            StartDateTime =datetime.now() + relativedelta(months=-1)
            StartDateTime = StartDateTime.strftime("%Y-%m-%d %H:%M:%S")
        #StartDateTime = StartDateTime + relativedelta(months=-1)
        
        qury = "exec pro.uspGetLocations  @productID={pID}, @ownerUserId = {owner},@sDate= '{SD}',@eDate='{ED}'".format(pID=ProductID or "Default",owner=OwnerID,SD=StartDateTime,ED=EndDateTime)

        print (qury)
        res = []
        self.cursor.execute(qury) 
        # self.cursor.commit()
        row = self.cursor.fetchone() 
        while row: 
            p =  locpoint(row[0],row[1],row[2],row[3],row[4],row[5])
            res.append(p)
            

            row = self.cursor.fetchone()
            
        
        return res


    def modifyLocation(self,productID,locationJson):
        """Modify location create and update"""
        try:
            query1 = "exec [pro].[uspModifyLocation] @ProductID=N'{prodID}' , @jsonLocationInput = N'{location}'".format(prodID=productID,location=locationJson)
            print(query1)
            self.cursor.execute(query1)
            self.cursor.commit()
        except Exception as X:
            print(X)
            return False
        
        return True




    def modifyServices(self,productID,serviceJson):
        """Modify location create and update"""
        try:
            query1 = "exec [pro].[uspModifyService] @ProductID=N'{prodID}' , @jsonServiceInput = N'{service}'".format(prodID=productID,service=serviceJson)
            print(query1)
            self.cursor.execute(query1)
            self.cursor.commit()
        except Exception as X:
            print(X)
            return False
        
        return True

    def getServices(self,productID):
        """get all Product servicsess of Online User that is avalable"""
        qury = "select s.sid,s.sname,s.sdescription,s.sprice,s.simage,s.sCreateDate,s.sUpdateDate,s.sOwnerPID,s.sOwnerMobile,s.sMobile,s.sType,s.sStatus,s.sProductID,s.sInstallerCode from pro.tblServices as s where s.sProductID = {productID}".format(productID=productID)
        res = []
        self.cursor.execute(qury) 
        row = self.cursor.fetchone() 
        while row: 
            p =  (row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9],row[10],row[11],row[12])    
            res.append(p)
            
            row = self.cursor.fetchone()
            
        
        return res


    def getServiceTitle(self):
        """get all Product servicsess of Online User that is avalable"""
        qury = "select servid, serviceName, [DateTime], updateTime, IsDeleted, isSystem from pro.[services]"
        self.cursor.execute(qury) 
        row = self.cursor.fetchone() 
        res = []
        while row: 
            p =  CarService()   
            p.servid=row[0]
            p.serviceName=row[1]
            p.DateTime=row[2]
            p.updateTime=row[3]
            p.IsDeleted=row[4]
            p.isSystem=row[5]
            res.append(p)
            
            row = self.cursor.fetchone()
            
        
        return res