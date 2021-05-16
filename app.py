# Import modules
import flask
from flask import Flask,jsonify,render_template
from flask.globals import request
from flask_pymongo import PyMongo
from pymongo import mongo_client

app= Flask(__name__)

# Set up mongoDb
uri='mongodb://localhost:27017/myDatabase'
mongodb_client=PyMongo(app,uri)
db=mongodb_client.db

# Routes
@app.route('/')
def home():
    return render_template('homepage.html')

@app.route('/signup',methods =["GET", "POST"])
def signup():
    if request.method=="POST":
        fname=request.form.get('fname')
        lname=request.form.get('lname')
        email=request.form.get('email')
        pass1=request.form.get('pass1')
        pass2=request.form.get('pass2')
        if pass1==pass2:
            db.users.insert_one({'fname':fname,'lname':lname,'email':email,'pass1':pass1,'pass2':pass2})
            return flask.jsonify(message='success')
        else:
            return flask.jsonify(message='failed')
    return render_template('index.html')

@app.route('/signin',methods =["GET", "POST"])
def signin():
    if request.method=="POST":
        email=request.form.get('email')
        pass1=request.form.get('pass1')
         
        user=db.users.find_one({"email":email})
        if user["pass1"]==pass1:
            
            return render_template('success.html',name=user["fname"])
        else:
            return render_template('fail.html')


    return render_template('signin.html')

# Run app
app.run(debug=True)