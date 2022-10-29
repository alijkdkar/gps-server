from datetime import datetime
import io
import os
import random
from flask import Flask, flash, jsonify, request, redirect, url_for
from sqlalchemy import null
from werkzeug.utils import secure_filename
from flask import send_from_directory
from flask import current_app

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER




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

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filename = getSecureFileName(file.filename)
            #path = current_app.root_path+"/"+app.config['UPLOAD_FOLDER']+
            print(os.path.join(current_app.root_path,app.config['UPLOAD_FOLDER'], filename))
            file.save(os.path.join(current_app.root_path,app.config['UPLOAD_FOLDER'], filename))
            return jsonify(f"file_name:{filename}")
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''
@app.route('/download/<path:filename>', methods=['GET', 'POST'])
def download(filename):
    uploads = os.path.join(current_app.root_path, app.config['UPLOAD_FOLDER'])
    return  send_from_directory(uploads, filename)




    
def getSecureFileName(orginalFileName:str):
    filename = datetime.now().strftime('%Y%m%d%H%M%S')
    return filename +"."+ orginalFileName.split(".")[1]


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    



if __name__ == '__main__':
    app.run(host="127.0.0.1",port= 555,debug=True, threaded=False)