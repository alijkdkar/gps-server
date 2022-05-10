import mysql.connector


class DbMySqlRepository:
        def __init__(self, host, user, password, database):
            self.host = host
            self.user = user
            self.password = password
            self.database = database
            self.cnxn = mysql.connector.connect(host=self.host, user=self.user, password=self.password, database=self.database)

        @staticmethod
        def getInstance():
            return DbMySqlRepository(host='localhost', user='sa', password='123456789', database='gpsManager')

            


        def checkConnection(self):
            try:
                self.cnxn.ping()
                mycursor = self.cnxn.cursor()
                print(mycursor.execute("SHOW DATABASES"))
                return True
            except Exception as X:
                print(X)
                return False


print(DbMySqlRepository.getInstance().checkConnection())