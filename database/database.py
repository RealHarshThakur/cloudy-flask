from flask_pymongo import PyMongo
from flask import Flask, request,jsonify, make_response
from flask_restplus import fields, Api, Namespace, Resource, marshal
import json
import os 

app = Flask(__name__)
mongodb_ip = os.environ["MONGODB_SERVICE_HOST"]
mongodb_port = os.environ["MONGODB_PORT_27017_TCP_PORT"]
app.config["MONGO_URI"] = "mongodb://"+mongodb_ip+":"+mongodb_port+"/users"
mongo = PyMongo(app)
db_ns = Namespace('database')
api = Api()
api.add_namespace(db_ns)
api.init_app(app)
users_model = db_ns.model('User Details',{
    'email': fields.String(required=True),
    'name': fields.String(required=True),
    'password': fields.String(required=True),
    'role': fields.String(required=True)
})

@db_ns.route('/')
class Data(Resource):
    
    @db_ns.doc('Retrives all data from the database')
    def get(self):
        db_users = mongo.db.users
        result = []
        for u in db_users.find():
            result.append({'username':u['name'],'password':u['password'],'email':u['email'],'role':u['role']})
        return result
    
    @db_ns.doc("Post data")
    @db_ns.expect(users_model)    
    def post(self):
        db_users = mongo.db.users
        username = db_ns.payload['name']
        password = db_ns.payload['password']
        email = db_ns.payload['email']
        role = db_ns.payload['role']
        email_finder = db_users.find_one({"email":email})
        if email_finder:
            return  make_response("Error:Email already taken", 404)
        else:
            data = {'name':username,'password':password,'email':email, 'role': role}
            db_users.insert(data)
            result = json.dumps(marshal(data, users_model,ordered=True))
            return make_response(jsonify("Msg:User added"), 200)
        
    @db_ns.doc('Deleted all data from the database')
    def delete(self):
        db_users = mongo.db.users
        result = []
        for u in db_users.find():
            result.append({'username':str(u['name'])})
            db_users.remove(u)
        return make_response(jsonify("Msg: Users deleted"),200)    

@db_ns.doc("email")
@db_ns.route('/<email>')
class Username(Resource):
    @db_ns.doc("Retrieves all the usernames")
    def get(self,email):
        db_users = mongo.db.users
        email_finder = db_users.find_one({"email":email})
        if email_finder:
            result = {'username': email_finder['name'],'password':email_finder['password'],'email':email_finder['email'],'role':email_finder['role']}
            return make_response(result,200)
        return make_response("Error:User not found",404)

    @db_ns.doc("Delete user")
    def delete(self,email):
        db_users = mongo.db.users
        email_finder = db_users.find_one({"email":email})
        if email_finder:
            db_users.remove(email_finder)
            deleted_user = {'User deleted':email_finder['name']}
            return make_response(jsonify("Msg: User deleted",200))
        else: 
            return make_response("Error:User not found",404)




  