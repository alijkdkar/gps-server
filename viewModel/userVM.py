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
        print('a')
        username = self.userName[0]
        print('b')
        name = self.name[0] or 'unname'
        print('c')
        lastName = self.lastName[0] or 'unlastname'
        print('d')
        displayName=name+' '+lastName
        
        query = """if not exists (select 1 from sec.users where userName='{usernamearg}' )
                   insert into sec.personel([Name],[LastName],[DisplayName]) values ('{namearg}','{LastNamearg}','{dsnamearg}')
                   """.format(usernamearg=username,namearg=name,LastNamearg=lastName,dsnamearg=displayName)
        print(query)
        cursor.execute(query)
        id = cursor.fetchone()[0]  # although cursor.fetchval() would be preferred
        cursor.commit()
        
        print('fffff')


        return id