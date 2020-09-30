#import Flask to create instance of web application
#request to get request data
#jsonify to turns the JSON output into a Response object with the application/json mimetype
#SQAlchemy from flask_sqlalchemy to accessing database
#Marshmallow from flask_marshmallow to serialized object
from flask import Flask, request, jsonify, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from datetime import datetime
import os

#Create an instances of our web application and set path of our SQLite uri.
app = Flask(__name__, template_folder="templates")
app.secret_key = "SecretKey20202020202020"
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data_test.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


#---- ---- ---- ----
#Binding SQLAlchemy and Marshmallow into our flask application.
db = SQLAlchemy(app)
ma = Marshmallow(app)
#---- ---- ---- ----
#After importing SQLAlchemy and bind it to our flask app, we can declare our models. Here we declare model called Data and defined its field with it's properties.
class Data(db.Model):
    __tablename__ = 'records'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(200), unique=False)
    email = db.Column(db.String(250), unique=False)
    timestamp = db.Column(
        db.DateTime, default=datetime.now(), onupdate=datetime.now()
    )

    def __init__(self, username, email):
#		self.id = id
        self.username = username
        self.email = email
        #self.timestamp = timestamp
#---- ---- ---- ----
#This part defined structure of response of our endpoint. We want that all of our endpoint will have JSON response. Here we define that our JSON response will have two keys(username, and email). Also we defined user_schema as instance of UserSchema, and user_schemas as instances of list of UserSchema.
class DataSchema(ma.Schema):
    class Meta:
        # Fields to expose
	# fields = ('username', 'email')
        #fields = ('id', 'username', 'email')
        fields = ('id', 'username', 'email', 'timestamp')

data_schema = DataSchema()
datas_schema = DataSchema(many=True)
#---- ---- ---- ----
#---- ---- ---- ----
# endpoint to show all records
@app.route("/data", methods=["GET"])
def get_data():
    all_data = Data.query.all()
    result = datas_schema.dump(all_data)
    return datas_schema.jsonify(all_data)
#---- ---- ---- ----
# endpoint to get user detail by id
@app.route("/data/<id>", methods=["GET"])
def data_detail_id(id):
    data = Data.query.get(id)
    return data_schema.jsonify(data)
#---- ---- ---- ----
# endpoint to get user detail by username
@app.route("/data/username/<username>", methods=["GET"])
def data_detail_username(username):
    #data = Data.query.get(id)
    data = Data.query.filter(Data.username == username).one_or_none()
    return data_schema.jsonify(data)
#---- ---- ---- ----
#endpoint to create new record
##set the route to "/data" and set HTTP methods to POST
@app.route("/data", methods=["POST"])
def add_data():
	#id = request.json[' id']
    username = request.json['username']
    email = request.json['email']
    
    new_data = Data(username, email)
    if db.session.query(Data).filter_by(username=username).count() > 0:
        return jsonify('This data exist on database!')

    db.session.add(new_data)
    db.session.commit()
    return jsonify('Data added Successfully!')
#---- ---- ---- ----
# endpoint to update a record
@app.route("/data/<id>", methods=["PUT"])
def data_update(id):
    data = Data.query.get(id)
	#id = request.json['id']
    username = request.json['username']
    email = request.json['email']

    data.username = username
    data.email = email


    db.session.commit()
    return data_schema.jsonify(data)
#---- ---- ---- ----
# endpoint to delete a record
@app.route("/data/<id>", methods=["DELETE"])
def data_delete(id):
    data = Data.query.get(id)
    db.session.delete(data)
    db.session.commit()

    return jsonify('Data was deleted!')
    #return data_schema.jsonify(user)
#---- ---- ---- ----
'''
#Make req with header: Content-Type : application/json
#read all data
curl 'http://127.0.0.1:5000/data'
#get user detail by id
curl 'http://127.0.0.1:5000/data/1'
#get user detail by username
curl 'http://127.0.0.1:5000/data/username/admin'
#create new record
curl 'http://127.0.0.1:5000/data' -H "Content-Type: application/json" -X POST -d '{ "email": "user1@localhost.local", "username": "user1" }'
#update a record by id
curl 'http://127.0.0.1:5000/data/1' -H "Content-Type: application/json" -X PUT -d '{ "email": "admin@localhost.local", "id": 1, "username": "admin1" }'
#delete a record by id
curl 'http://127.0.0.1:5000/data/7' -X DELETE
'''


