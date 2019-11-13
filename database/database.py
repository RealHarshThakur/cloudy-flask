from flask_pymongo import PyMongo
from flask import Flask, request,jsonify
from flask_restplus import fields, Api, Namespace, Resource, marshal
import json

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/users"
mongo = PyMongo(app)
db_ns = Namespace('database')
api = Api()
api.add_namespace(db_ns)
api.init_app(app)
users_model = db_ns.model('User Details',{
    'email': fields.String(required=True),
    'name': fields.String(required=True),
    'password': fields.String(required=True)
})

@db_ns.route('/')
class Data(Resource):
    
    @db_ns.doc('Retrives all data from the database')
    def get(self):
        db_users = mongo.db.users
        result = []
        for u in db_users.find():
            result.append({'username':u['name'],'password':u['password'],'email':u['email']})
        return result
    
    @db_ns.doc("Post data")
    @db_ns.expect(users_model)    
    def post(self):
        db_users = mongo.db.users
        username = db_ns.payload['name']
        password = db_ns.payload['password']
        email = db_ns.payload['email']
        email_finder = db_users.find_one({"email":email})
        if email_finder:
            return "Error:Email already taken"
        else:
            data = {'name':username,'password':password,'email':email}
            db_users.insert(data)
            result = json.dumps(marshal(data, users_model,ordered=True))
            return result
        
    @db_ns.doc('Deleted all data from the database')
    def delete(self):
        db_users = mongo.db.users
        result = []
        for u in db_users.find():
            result.append({'username':str(u['username'])})
            db_users.remove(u)
        return result    

@db_ns.doc("email")
@db_ns.route('/<email>')
class Username(Resource):
    @db_ns.doc("Retrieves all the usernames")
    def get(self,email):
        db_users = mongo.db.users
        email_finder = db_users.find_one({"email":email})
        if email_finder:
            result = {'username': email_finder['name'],'password':email_finder['password'],'email':email_finder['email']}
            return result
        return {"Error:User not found"},404

    @db_ns.doc("Delete user")
    def delete(self,email):
        db_users = mongo.db.users
        email_finder = db_users.find_one({"email":email})
        if email_finder:
            db_users.remove(email_finder)
            deleted_user = {'User deleted':email_finder['name']}
            return deleted_user
        else: 
            return "Error:User not found",404




  