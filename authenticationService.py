from crypt import methods
from flask import Flask,request
from flask_cors import CORS
from sqlalchemy import true
from viewModel.ViewModels import db
from viewModel.tokenVm import  Token
from functools import wraps



# db = SQLAlchemy()
app = Flask(__name__)
CORS(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
# initialize the app with the extension
db.init_app(app)



def require_api_key(api_method):
    @wraps(api_method)

    def check_api_key(*args, **kwargs):
        apikey = request.headers.get('ApiKey') if request.args.get("token",default="0",type=str) else request.headers.get('ApiKey')
        print("hiiiiiii")
        print(apikey)
        print("bye")
        
        if apikey and checktokenToken(apikey):
            return api_method(*args, **kwargs)
        else:
            return None

    return check_api_key


def checktokenToken(token):
    print("check token",token)
    if token is None or  token == "0" :
      return False
    return Token.checkToken(token)


@app.route("/")
@require_api_key
def home():
    return "Hello, Flask!"

@app.route("/getToken",methods=["GET"])
def getToken():
    return Token.create_new_HashToken() 


# if __name__ == "__main__":
    # app.run()
if __name__ == '__main__':
  app.run(host='127.0.0.1', port=8000, debug=True, threaded=False)