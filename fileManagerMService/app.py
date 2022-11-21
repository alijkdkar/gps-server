from datetime import datetime
import os
from flask import Flask, flash, jsonify, request, redirect, url_for
from werkzeug.utils import secure_filename
from flask import send_from_directory
from flask import current_app
import base64
import redis 
import struct
import binascii

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
ALLOWED_EXTENSIONS_MAGIC_NUMBER = {'txt':'EF BB BF'
                                    , 'pdf':'25 50 44 46 2D'
                                    , 'png':'89 50 4E 47 0D 0A 1A 0A'
                                    , 'jpg':'FF D8 FF E0'
                                    , 'jpeg':'FF D8 FF'
                                    , 'gif':'47 49 46 38 37 61'}


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# app.config['REDIS_HOST'] = '127.0.0.1'
# app.config['REDIS_PORT'] = 6379
# app.config['REDIS_DB'] = 0
#redis1 = Redis(app)

#redis1 = redis.Redis(host="some-redis",port="6379",db=0)
redis1 = redis.Redis(host="127.0.0.1",port="6379",db=0)

#todo : comperess image on save
#todo : comperess image on load
#todo : face detection on image
#todoooo : save date time of modiy images
#todo : search on images
#todo : load images as list
#todooo : load images as base64
#Done : redefine redise db

@app.route('/repair', methods=['GET', 'POST'])
def repair_redis():
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    files =os.listdir(app.config['UPLOAD_FOLDER'])
    for file in files:
        
        if file.count('.')>0:
            if (redis1.get(str(file).split(".")[0]) or b'').decode("utf-8") != file :
                redis1.set(str(file).split(".")[0],str(file))
        else:
            if (redis1.get(str(file)) or b'').decode("utf-8") != file :
                redis1.set(str(file),str(file))

    return """{{status:200,msg:"success "}}"""
        
    


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            return """{{status:200,msg:"No selected file"}}"""
        
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            return """{{status:200,msg:"No selected file"}}"""
        
        if not os.path.exists(app.config['UPLOAD_FOLDER']):
            os.makedirs(app.config['UPLOAD_FOLDER'])
        
        print(">>>>",file.headers)
        
        
        if file and allowed_file(file.filename):
            filename, justfileName = saveFileOnDirectory(file)
            if filename is None or justfileName is None:
                return """{{status:200,msg:"File extention has damaged"}}"""
            return jsonify(f"file_name:{justfileName}")
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''

def saveFileOnDirectory(file):
    filename = secure_filename(file.filename)
    justfileName ,filename = getSecureFileName(file.filename)
            #path = current_app.root_path+"/"+app.config['UPLOAD_FOLDER']+
    filePath = os.path.join(current_app.root_path,app.config['UPLOAD_FOLDER'], filename)
    file.save(filePath)
    if checkFileRealExtention(fileName=filePath):
        redis1.set(justfileName,filename)
        return filename,justfileName
    else:
        os.remove(filePath)
        return None,None




### begin ### down load 

@app.route('/download/<path:filename>', methods=['GET', 'POST'])
def download(filename:str):
    if "." in filename:
        return """{{status:200,msg:"wrong file name"}}"""
    orginalFileName = check_res_db(filename) 
    if (orginalFileName or "") == "":
        return """{{status:200,msg:"file not exits"}}"""
    uploadsurl = getUploadUrl()
    file = send_from_directory(uploadsurl, str(orginalFileName))
    return file


# @app.route('/downloadBase64/<path:fileID>', methods=['GET', 'POST'])
# def downloadBase64(fileID:str):
#     if "." in fileID:
#         return """{{status:200,msg:"wrong file name"}}"""
#     db_fileName = check_res_db(fileID)
#     if (db_fileName or "")=="":
#         return """{{status:200,msg:"file not exits"}}"""
#     imagedata=""
#     uploadsurl = getUploadUrl()
#     #file = send_from_directory(uploadsurl, str(db_fileName))
#     print(os.path.join(uploadsurl, str(db_fileName))+".jpeg")
#     with open(os.path.join(uploadsurl, str(db_fileName)), "wb") as fh:
#         fh.write(base64.decodebytes(imagedata+".jpeg"))
#     return imagedata


def getUploadUrl():
    uploadsurl = os.path.join(current_app.root_path, app.config['UPLOAD_FOLDER'])
    return uploadsurl



def check_res_db(filename):
    orginalFileName = redis1.get(filename)
    orginalFileName = orginalFileName.decode("utf-8")
    return orginalFileName



### end ### download


    
def getSecureFileName(orginalFileName:str):
    filename = datetime.now().strftime('%Y%m%d%H%M%S')
    return filename,filename +"."+ orginalFileName.split(".")[1]


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    
def checkFileRealExtention(fileName):
    fileExt = getFileFileExtention(fileName)
    magicNum = ALLOWED_EXTENSIONS_MAGIC_NUMBER[fileExt]
    with open(fileName, mode='rb') as file: # b is important -> binary
        fileContent = file.read()
        header = str(binascii.hexlify(fileContent))[2:-1]
    if header.startswith(magicNum):
        return True
    else:
        return False



def getFileFileExtention(file):
    if '.' in file:
        return file and file.split(".")[1]
    else:
        return None
    




if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0', port=5055)