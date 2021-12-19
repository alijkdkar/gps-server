import pyodbc 



# connection to db
class dbEntity:
    def __init__(self) -> None:
        server = '.\SQLEXPRESS2014' 
        database = 'gpsDB' 
        username = 'sa' 
        password = '123456789' 



    def openConnection(self):
        
        cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER='+self.server+';DATABASE='+self.database+';UID='+self.username+';PWD='+ self.password)
        cursor = cnxn.cursor()
        cursor.execute('select * from settings')
        for i in cursor:
            print(i)

        return