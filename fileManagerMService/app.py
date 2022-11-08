from datetime import datetime
import os
from flask import Flask, flash, jsonify, request, redirect, url_for
from werkzeug.utils import secure_filename
from flask import send_from_directory
from flask import current_app
import redis 


UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# app.config['REDIS_HOST'] = '127.0.0.1'
# app.config['REDIS_PORT'] = 6379
# app.config['REDIS_DB'] = 0
#redis1 = Redis(app)
redis1 = redis.Redis(host="some-redis",port="6379",db=0)




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

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            justfileName ,filename = getSecureFileName(file.filename)
            #path = current_app.root_path+"/"+app.config['UPLOAD_FOLDER']+
            print(os.path.join(current_app.root_path,app.config['UPLOAD_FOLDER'], filename))
            file.save(os.path.join(current_app.root_path,app.config['UPLOAD_FOLDER'], filename))
            redis1.set(justfileName,filename)
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






@app.route('/download/<path:filename>', methods=['GET', 'POST'])
def download(filename:str):
    if "." in filename:
        return """{{status:200,msg:"wrong file name"}}"""
    print(filename)
    orginalFileName = redis1.get(filename)
    orginalFileName = orginalFileName.decode("utf-8") 
    if (orginalFileName or "") == "":
        return """{{status:200,msg:"file not exits"}}"""
    uploads = os.path.join(current_app.root_path, app.config['UPLOAD_FOLDER'])
    return  send_from_directory(uploads, str(orginalFileName))




    
def getSecureFileName(orginalFileName:str):
    filename = datetime.now().strftime('%Y%m%d%H%M%S')
    return filename,filename +"."+ orginalFileName.split(".")[1]


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    



if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0', port=5055)