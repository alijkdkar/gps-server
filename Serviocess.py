
from ast import Str
from asyncio.windows_events import NULL
from typing import Hashable, List, Text
from flask import Flask , request, jsonify
import base64
import io
from flask_cors import CORS
# from mViewModels import Settingg, User
import json
from matplotlib.style import use
import pyodbc
from dBRepository import dbEntity 
import myutils as utils
from viewModel.mViewModels import Settingg
from viewModel.tokenVm import  Token
from viewModel.userVM import   User
from viewModel.productsVM import  product as ProductVm
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



@app.route("/signUPWithCrential",methods=["POST"])
def signUPWithCrential():
  crential =request.args.get("crential",default="0",type=str)
  #password =request.args.get("password",default="0",type=str)

  if crential == "0" :
    return "{status:invalid requst !}"
  #ss = AESCipher("662ede816988e58fb6d057d9d85605e0").encrypt("ali")
  dd = AESCipher(constes.CryptionKey).decrypt(crential.replace(" ","+"))
  u = Token().fillByJson(jsonData=dd)
  newUser=User().GetUserFromDbByUserName(username= u.userName)
  personID = None 
  if newUser is None or newUser.id is None:
    user = User(u.userName,u.password ,u.Display,"",None,"",123,None)
    personID= db.signUpMember(userp=user)
    #todo : Create Token For this user and retrun
  db.SaveToken(PersonelID=personID or newUser.personelID or user.personelID,token= u.tokenString)
  return  f"""{{"status":"200","userInfo":{str(newUser.userJsonString or user.userJsonString)},"token":"{str(u.tokenString).strip()}"}}""".strip("\n")#.format(oken={str(u.tokenString)}) 


@app.route("/signInWithCrential",methods=["POST"])
def signInWithCrential():
  crential =request.args.get("crential",default="0",type=str)
  #password =request.args.get("password",default="0",type=str)

  if crential == "0" :
    return "{status:invalid requst !}"
  #ss = AESCipher("662ede816988e58fb6d057d9d85605e0").encrypt("ali")
  dd = AESCipher(constes.CryptionKey).decrypt(crential.replace(" ","+"))
  u = Token().fillByJson(jsonData=dd)
  newUser=User().GetUserFromDbByUserName(username= u.userName)
  if newUser.id is None:
    #user = User(u.userName,u.password ,u.Display,"",None,"",123,None)
    # personID= db.signUpMember(userp=user)
    return  f"""{{status:401,userInfo:"",token:""}}""".strip("\n")
    #todo : Create Token For this user and retrun
  db.SaveToken(newUser.personelID,token= u.tokenString)
  return  f"""{{"status":"200","userInfo":{str(newUser.userJsonString)},"token":"{str(u.tokenString).strip()}"}}""".strip("\n")#.format(oken={str(u.tokenString)}) 


def checktokenToken(token):
    #token =request.args.get("token",default="0",type=str)
    if token is None or  token == "0" :
      return False
    return Token.checkToken(token)
  


@app.route("/signInWithUserPass",methods=["POST"])
def signInWithUserPass():
  username =request.args.get("username",default="",type=str)
  password =request.args.get("password",default="",type=str)

  if username == "" or password =="":
    return  f"""{{status:400,userInfo:"",token:""}}""".strip("\n")#.format(oken={str(u.tokenString)}) 
  
  user, token  = db.signInWithPassword(username,password)
  if user is None or token is None:
    return  f"""{{status:401,userInfo:"",token:""}}""".strip("\n")

  return  f"""{{"status":"200","userInfo":{str(user.userJsonString )},"token":"{str(token.tokenString).strip()}"}}""".strip("\n")



@app.route("/ModifyProduct",methods=["POST"])
def ModifyProduct():
  token =request.args.get("token",default="",type=str)
  productKson =request.args.get("productJson",default="",type=str)
  pImage =request.args.get("pImage",default= None,type=Str)
  if token == "" or token =="":
    return  f"""{{status:401,msg:"bad Requst"}}""".strip("\n")
  
  imageAddress=""
  filename = saveImageinDirectory(pImage)
  # if pImage is not NULL:
    # with open(r"assets\uplaodedImages\imageToSave.png", "wb") as fh:
    #    fh.write(base64.b64decode (pImage))
    # imageAddress = r"assets\uplaodedImages\imageToSave.png"

  print("@@@@@@@@@@@\n")
  d = json.loads(productKson)
  # for d in jdata:
    # product = ProductVm(d['pid'],str (d['pname']),d['pOwnerMobile'],d['pOwnerPID'],d['pMobile'],d['ptype'],d['pimage'],d['mimiSerial'],d['pcreateDate'],d['pUpdateDate'],d['installerCode'])
  product = ProductVm(d['pid'],str (d['pname']),d['pownerMobile'],d['pOwnerPID'],d['pMobile'],d['ptype'],filename,d['mimiSerial'],d['pcreateDate'],d['pUpdateDate'],d['installerCode'])
  json.dumps(product.__dict__,ensure_ascii=True)
    # for key,value in enumerate(d):
    #       print(d[value])
  dbEntity().saveProduct(product=product)

  return   f"""{{status:200,msg:"products Added Success"}}""".strip("\n")

def saveImageinDirectory(pImage):
  if pImage is not None:
    pImage1= pImage.value.replace(' ','+')
    imgdata = base64.b64decode(pImage1)
    picname=Str(datetime.now().strftime("%H%M%S"))
    filename = r'assets\uplaodedImages\{fileName}.png'.format(fileName=picname.value)  
    with open(filename, 'wb') as f:
      f.write(imgdata)
    return filename
  return ""
  
  #return  f"""{{"status":"200","userInfo":{str(user.userJsonString )},"token":"{str(token.tokenString).strip()}"}}""".strip("\n")#.format(oken={str(u.tokenString)}) 




@app.route("/getOwnerProducts",methods=["GET","POST"])
def getOwnerProducts():
  token =request.args.get("token",default="",type=str)
  productID =request.args.get("productID",default=None,type=int)

  if token == "" or token =="":
    return  f"""{{status:401,msg:"bad Requst"}}""".strip("\n")
  
  if Token().checkToken(token=token) == True:
    tokenobj =  Token().create(token)
    productList = db.getProducts(tokenobj.id,productID or None)

    #json_string = json.dumps(productList, indent=4, sort_keys=True, default=str)
    json_string = json.dumps([ob.__dict__ for ob in productList], indent=4, sort_keys=True, default=str,ensure_ascii=False)


  
  return """{{status:200,msg:"query Success",payload:{json_string}}}""".format(json_string = json_string) 




@app.route("/getLocations",methods=["POST"])
def getLocations():
  token =request.args.get("token",default="",type=str)
  productID =request.args.get("productID",default=None,type=int)
  
  if token == "" or token =="":
    return  f"""{{status:401,msg:"bad Requst"}}""".strip("\n")
  
  if Token().checkToken(token=token) == True:
    tokenobj =  Token().create(token)

  productList = db.getProducts(tokenobj.id,productID or None)
  locs = db.getProductsHisLoc(OwnerID=tokenobj.id,ProductID=productID or None)
  totalstring ="["
  
  for x in productList:
    #for y in filter(lambda z: z.ProductID==x.pid ,locs):
    jsstring= json.dumps(x.__dict__, indent=4, sort_keys=True, default=str,ensure_ascii=False)
    ll = loctionJsonString = json.dumps([ob.__dict__ for ob in filter(lambda z: z.ProductID==x.pid ,locs)], indent=4, sort_keys=True, default=str,ensure_ascii=False)
    jsstring= jsstring.replace('"BBLLoCEDA"',ll)
    totalstring+=(jsstring+",")
    #json.dumps([ob.__dict__ for ob in locs], indent=4, sort_keys=True, default=str,ensure_ascii=False)
        #jsstring += json.dumps(y.__dict__, indent=4, sort_keys=True, default=str,ensure_ascii=False)
  if len(totalstring)>1:
    totalstring = totalstring[:-1]
  totalstring += "]"
  
  # productJsonString = json.dumps([ob.__dict__ for ob in productList], indent=4, sort_keys=True, default=str,ensure_ascii=False)
  

  return """{{status:200,msg:"query Success",payload:{json_string}}}""".format(json_string =totalstring) 


@app.route("/modifyLocation",methods=["POST"])
def modifyLocation():
  token =request.args.get("token",default="",type=str)
  productID =request.args.get("productID",default=None,type=int)
  locationJson =request.args.get("locationJson",default="",type=str)
  if token == "" or token =="":
    return  f"""{{status:401,msg:"bad Requst"}}""".strip("\n")
  
  if Token().checkToken(token=token) == True:
    tokenobj =  Token().create(token)
    db.modifyLocation(productID or tokenobj.id,locationJson)
  
  return f"""{{status:200,msg:"query Success",payload:[]}}"""


@app.route("/modifyServices",methods=["GET"])
def modifyServices():
  token =request.args.get("token",default="",type=str)
  productID =request.args.get("productID",default=None,type=int)
  servicesJson =request.args.get("servicesJson",default=None,type=str)
  print("_________",servicesJson,"_________")
  if token == "" or token =="":
    return  f"""{{status:401,msg:"bad Requst"}}""".strip("\n")
  
  if Token().checkToken(token=token) == True:
    tokenobj =  Token().create(token)
    db.modifyServices(productID or tokenobj.id,servicesJson)
  
  return f"""{{status:200,msg:"query Success",payload:[]}}"""


@app.route("/GetServicesTitle",methods=["GET"])
def GetServicesTitle():
  
  res =db.getServiceTitle()
  resualt = json.dumps([ob.__dict__ for ob in res], indent=4, sort_keys=True, default=str,ensure_ascii=False)
  return """{{status:200,msg:"query Success",payload:{json_string}}}""".format(json_string =resualt) 


@app.route("/GetServiceDetails",methods=["GET"])
def GetServiceDetails():
  token =request.args.get("token",default="",type=str)
  productID =request.args.get("productID",default=None,type=int)
  print(productID)
  if token == "" or token =="":
    return  f"""{{status:401,msg:"bad Requst"}}""".strip("\n")
  
  if Token().checkToken(token=token) == True:
    tokenobj =  Token().create(token)
    res =db.getServiceDetails(productID or tokenobj.id)
    resualt = json.dumps([ob.__dict__ for ob in res], indent=4, sort_keys=True, default=str,ensure_ascii=False)
    return """{{status:200,msg:"query Success",payload:{json_string}}}""".format(json_string =resualt)


@app.route("/getWrongArea",methods=["GET"])
def getWrongArea():
    token =request.args.get("token",default="",type=str)
    productID =request.args.get("productID",default=None,type=int)
    if token == "" or token =="":
      return  f"""{{status:401,msg:"bad Requst"}}""".strip("\n")
    if Token().checkToken(token=token) == True:
      tokenobj =  Token().create(token)
      res = db.getWrongArea(productID or tokenobj.id)
      resualt = json.dumps([ob.__dict__ for ob in res], indent=4, sort_keys=True, default=str,ensure_ascii=False)
      return """{{status:200,msg:"query Success",payload:{json_string}}}""".format(json_string =resualt)
    

# if __name__ == "__main__":
    # app.run()
if __name__ == '__main__':
  app.run(host='192.168.1.110', port=5000, debug=True, threaded=False)