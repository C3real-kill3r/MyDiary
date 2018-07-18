from flask import *
from functools import wraps
import datetime

app = Flask(__name__)
user={}
diary_content={}

app.config['SECRET_KEY'] = 'brybzlee'

@app.route ('/api/v1/',methods=['GET'])
def home():
    return jsonify({'message' : 'welcome to your diary'})

@app.route ('/api/v1/register',methods=['POST'])
def register():
    name =request.get_json()["name"]
    username =request.get_json()["username"]
    email =request.get_json()["email"]
    password =request.get_json()["password"]

    if username not in user:
        user.update({username:{"name":name,"email":email,"password":password}})
        return jsonify(user)
    else:
            return jsonify({'message' : 'username already exist'})

def login_authorization(username, password):
    if username in user:
        if password == user[username]["password"]:
            return True
    return False

def replace (old,new,lst):
    for each in lst:
        if each == old:
            index=lst.index(each)
            del lst[index]
            lst.insert(index,new)


def logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' not in session:
            return jsonify({'message' : 'please login to continue'})
        else:
            return f(*args, **kwargs)
    return wrap

@app.route ('/api/v1/login',methods=['POST'])
def login():
    username=request.get_json()["username"]
    password=request.get_json()["password"]
    if login_authorization(username, password):
        session['logged_in'] = True
        session['username'] = username
        return jsonify({'message' : 'welcome to your diary'}) 
    else:
        return jsonify({'message' : 'invalid credentials'})

@app.route ('/api/v1/make_entry',methods=['POST'])
@logged_in
def make_entry():
    username=session.get('username')
    entry=request.get_json()["entry"]
    if username not in diary_content:
        diary_content.update({username:[]})
    diary_content[username].append(entry)
    return jsonify({'message' : 'diary successfully updated'})

@app.route ('/api/v1/get_all',methods=['GET'])
@logged_in
def get_all():
    username=session.get('username')
    output={}
    for each in diary_content[username]:
        output.update({diary_content[username].index(each)+1:each})
    return jsonify (output)

@app.route ('/api/v1/get_one/<int:entryID>',methods=['GET'])
@logged_in
def get_one(entryID):
    username=session.get('username')
    return jsonify({entryID:diary_content[username][entryID-1]})


@app.route ('/api/v1/modify_entry/<int:entryID>',methods=['PUT'])
@logged_in
def modify_entry(entryID):
    entry=request.get_json()["entry"]
    username=session.get('username')
    old=diary_content[username][entryID-1]
    replace (old, entry,diary_content[username])
    return jsonify({'message' :'entry successfully modified'})

@app.route ('/api/v1/delete_entry/<int:entryID>',methods=['DELETE'])
@logged_in
def delete_entry(entryID):
    username=session.get('username')
    del diary_content[username][entryID-1]
    return jsonify ({'message' : 'succesfully deleted'})

@app.route ('/api/v1/logout',methods=['GET'])
@logged_in
def logout():
    session.clear()
    return jsonify({'message' : 'you are successfully logged out'})

if __name__== '__main__':
    app.run(debug=True)