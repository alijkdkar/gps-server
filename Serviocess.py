
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
from mViewModels import Settingg, Token, User
from hashlab import AESCipher
#import hashlib as hasher
import pandas as pd





from datetime import datetime
import re


app = Flask(__name__)
CORS(app)


@app.route("/")
def home():
    return "Hello, Flask!"




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
  dd = AESCipher("662ede816988e58fb6d057d9d85605e0").decrypt(crential)


  
  u = Token(jsonData=dd)
  #todo : Create Token For this user and retrun

  return str( u.tokenString)

#@app.route("/checktokenToken",methods=["POST"])
def checktokenToken():
    token =request.args.get("token",default="0",type=str)
    if token == "0" :
      return "{Status:invalid requst !}"
    res = Token.checkToken(token)
    return str(res)



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