import pyodbc 
import pandas as pd

from viewModel.mViewModels import Settingg


# connection to db
class dbEntity:
    def __init__(self):
        self.server = '.\SQLEXPRESS2014' 
        self.database = 'gpsDB' 
        self.username = 'sa' 
        self.password = '123456789' 
        self.cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER='+self.server+';DATABASE='+self.database+';UID='+self.username+';PWD='+ self.password)
        #cursor = cnxn.cursor()


    def getSetting(self,customerID):
        #self.cursor.execute('select * from settings')
        if customerID is None:
            df = pd.read_sql_query("select * from settings",self.cnxn)
        else:
            df = pd.read_sql_query("select * from settings where customerID ="+str( customerID),self.cnxn)


        listofSetting= [(Settingg(row.id,row.name,row.value,row.Description)) for index, row in df.iterrows() ]  

        return listofSetting
    
    def signUpMember(self):
        
        
        
        return True