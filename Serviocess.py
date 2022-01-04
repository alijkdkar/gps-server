
from typing import Hashable, List, Text
from flask import Flask , request, jsonify
import base64
import io
from flask_cors import CORS
# from mViewModels import Settingg, User
import json
import pyodbc
from dBRepository import dbEntity 
import myutils as utils
from viewModel.mViewModels import Settingg
from viewModel.tokenVm import  Token
from viewModel.userVM import   User
from hashlab import AESCipher
#import hashlib as hasher
import pandas as pd
from functools import wraps
import constes





from datetime import datetime
import re


app = Flask(__name__)
CORS(app)
db = dbEntity()

@app.route("/")
def home():
    return "Hello, Flask!"


def require_api_key(api_method):
    @wraps(api_method)

    def check_api_key(*args, **kwargs):
        apikey = request.headers.get('ApiKey') if request.args.get("token",default="0",type=str) else request.headers.get('ApiKey')
        
        #token =request.args.get("token",default="0",type=str)
        if apikey and checktokenToken(apikey):
            return api_method(*args, **kwargs)
        else:
            return None

    return check_api_key


@app.route("/getSettings/",methods=["GET"])
def getSettings():
    cID = request.args.get("customerId",default="0",type=str)

    # sett =  Settingg(1,"testOption",1,"description",1)
    # settList = [sett,sett,sett,sett,sett]
    sitt =[""]

   
    # server = '.\SQLEXPRESS2014' 
    # database = 'gpsDB' 
    # username = 'sa' 
    # password = '123456789' 
    # cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
    # #cursor = cnxn.cursor()
    # #cursor = cnxn.cursor()
    # #cursor.execute('select id,name,value,Description from settings')
    # df = pd.read_sql_query("select id,name,value,Description from settings",cnxn)
    
    # print(df['name'])
    settList = dbEntity().getSetting()
    for x in settList:
        sitt.append(x.toJson())

    return json.dumps(sitt) #sett.toJson()





@app.route("/validationSMS",methods=["POST"])
def validationSMS():
  UserName =request.args.get("username",default="0",type=str)
  #password =request.args.get("password",default="0",type=str)

  if UserName == "" :
    return "invalid requst !"
  
  # todo: insert to db 
  # token = utils.createToken()
  CODE = utils.createvalidationCode()
  print(CODE)
  utils.sendSms(UserName, str( CODE))




  return "{Code:"+ str(CODE)  +"}"



@app.route("/signInWithCrential",methods=["POST"])
def signInWithCrential():
  crential =request.args.get("crential",default="0",type=str)
  #password =request.args.get("password",default="0",type=str)

  if crential == "0" :
    return "{status:invalid requst !}"
  #ss = AESCipher("662ede816988e58fb6d057d9d85605e0").encrypt("ali")
  dd = AESCipher(constes.CryptionKey).decrypt(crential)


  
  u = Token(jsonData=dd)
  print(u)
  print('asdasdasd')
  user = User(u.userName,"",u.Display,"",None,"",123,None)
  
  personID = db.signUpMember(userp=user)
  #todo : Create Token For this user and retrun
  db.SaveToken(PersonelID=personID,token= u.tokenString)
  return str( u.tokenString)


def checktokenToken(token):
    #token =request.args.get("token",default="0",type=str)
    if token is None or  token == "0" :
      return False
    return Token.checkToken(token)
  




# def Login(mobile,Password,token):
#   if mobile =="" :
#     return "invalid Requst!"
#   if Password =="":
#     code  = utils.createvalidationCode()
#     utils.sendSms(mobile,code)
#     return code ##todo : encript code

#   #todo : check username and password to DB
#   token = utils.createToken()
#   return token



# #api
# def forgetPassword(mobile):
#     code = utils.createvalidationCode()
#     utils.sendSms(mobile,code)
#     return code #encript code first

# #api
# def cheangePassword(mobile,newPassword):
#     #todo : change password on db

#     return True


# if __name__ == "__main__":
#     app.run(debug=True)
if __name__ == '__main__':
    app.run(host='192.168.1.107', port=5000, debug=True, threaded=False)