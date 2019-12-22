from flask import Flask, request,jsonify
from flask_restplus import fields, Api, Namespace, Resource,marshal
from flask_bcrypt import Bcrypt
from validate_email import validate_email
import requests
import json
import os

databasesvc_url = os.environ["DATABASE_SERVICE_HOST"]
databasesvc_port = os.environ["DATABASE_PORT_5000_TCP_PORT"]
database_url = "http://"+databasesvc_url+":"+ databasesvc_port + "/database"
app = Flask(__name__)
bcrypt = Bcrypt(app)
ns = Namespace('users')
users_model = ns.model('User Details',{
    'email': fields.String(required=True),
    'name': fields.String(required=True),
    'password': fields.String(required=True)
})
api = Api()
api.add_namespace(ns)
api.init_app(app)

@ns.route('/')
class User(Resource):    
    @ns.doc('List all users')
    def get(self):
        r = requests.get(database_url)
        user_data = r.json()
        return jsonify(user_data)

    @ns.doc('Add users')
    @ns.expect(users_model)
    def post(self):
        unvalidated_email = ns.payload['email']
        is_valid = validate_email(unvalidated_email)
        if is_valid:
            email = unvalidated_email
        else:
            return "Email address is not valid"
        username = ns.payload['name']
        password = ns.payload['password']
        r = requests.get(database_url)
        user_data = r.json()
        for user in user_data:
            if(email==user['email']):
                return jsonify("Error:Email already taken")
        password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
        data = {'name':username,'password':password_hash,'email':email}
        rp = requests.post(url=database_url, json=data)
        result = rp.json()
        return result
    
@ns.route('/<email>')
@ns.param('email','User email id')
@ns.response(404,'User not found')
class Username(Resource):
    @ns.doc('List the particular user given the email id')
    def get(self, email):
        url = database_url+email
        r = requests.get(url = url)
        result = r.json()
        return result
    
    @ns.doc('Deletes a user by taking a username as input')
    def delete(self,email):
        url = database_url+email
        r = requests.get(url = url)
        result = r.json()
        return result
    
