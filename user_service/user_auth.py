from flask import Flask, request,jsonify, make_response
from flask_restplus import fields, Api, Namespace, Resource,marshal
from flask_bcrypt import Bcrypt
from validate_email import validate_email
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token, jwt_optional, create_refresh_token, jwt_refresh_token_required, fresh_jwt_required,
    get_jwt_identity, get_jwt_claims, verify_jwt_in_request, get_raw_jwt
)
from functools import wraps
import requests
import json
import os

# Database service discovery
databasesvc_url = os.environ["DATABASE_SERVICE_HOST"]
databasesvc_port = os.environ["DATABASE_PORT_5000_TCP_PORT"]
database_url = "http://"+databasesvc_url+":"+ databasesvc_port + "/database/"

# Email service discovery 
emailsvc_url = os.environ["EMAIL_PORT_7000_TCP_ADDR"]
emailsvc_port = os.environ["EMAIL_SERVICE_PORT"]
email_url = "http://"+emailsvc_url+":"+emailsvc_port+"/email/"

# Boilerplate 
app = Flask(__name__)
bcrypt = Bcrypt(app)

api = Api()
api.init_app(app)

# Secret keys 
app.config['JWT_SECRET_KEY'] = 'super-secret' # Will use Hashicorp's Vault or kubenetes secrets later to store this 
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
jwt = JWTManager(app)
blacklist = set()

# Namespaces
ns = Namespace('users')
login_ns = Namespace('login')
register_ns = Namespace('register')
refresh_ns = Namespace('refresh')
freshlogin_ns = Namespace('fresh-login')
logout_ns = Namespace('logout')

# Models

users_model = ns.model('User Details',{
    'email': fields.String(required=True),
    'name': fields.String(required=True),
    'password': fields.String(required=True),
    'role': fields.String(required= False)
})


login_model = login_ns.model('Login Details',{
    'email': fields.String(required=True),
    'password': fields.String(required=True)
})


api.add_namespace(ns)
api.add_namespace(login_ns)
api.add_namespace(register_ns)
api.add_namespace(refresh_ns)
api.add_namespace(freshlogin_ns)
api.add_namespace(logout_ns)

@jwt.user_claims_loader
def regular_user(identity):
    return {
        'user': identity,
        'role': 'user'
    }

@jwt.user_claims_loader
def admin(identity):
    return {
        'user': identity,
        'role': 'admin'
    }

@jwt.user_claims_loader
def root(identity):
    return {
        'user': identity,
        'role': 'root'
    }

def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt_claims()
        print(claims)
        if (claims['role'] != 'admin') and (claims['role']!= 'root'): 
            return make_response(jsonify(msg="Admin or root only"), 403)
        else:
            return fn(*args, **kwargs)
    return wrapper



def root_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt_claims()
        if claims['role'] != 'root':
            return make_response(jsonify(msg="Only root"),403)
        else:
            return fn(*args, **kwargs)
    return wrapper

@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return jti in blacklist


@login_ns.route('/')
class Login(Resource):
    @login_ns.doc('Login')
    @login_ns.expect(login_model)
    @jwt_optional
    def post(self):
        current_user = get_jwt_identity()
        if current_user:
            return make_response(jsonify("Msg: You're logged in"), 200)
        else:
            email = login_ns.payload['email']
            password = login_ns.payload['password']
            r = requests.get(database_url+email)
            print(database_url+email)
            if r.status_code == 200:
                user_data = r.json()
                validate_password = bcrypt.check_password_hash(user_data['password'],password)
                if validate_password:
                    if (user_data['role']=="user"):
                        ret = {
                            'access_token':
                        create_access_token(identity=email, user_claims=regular_user(email),fresh=True),
                         'refresh_token': 
                        create_refresh_token(identity=email, user_claims=regular_user(email))
                        }

                        return make_response(jsonify(ret), 200)
                    elif (user_data['role']=="admin"):
                        ret = {
                            'access_token': 
                            create_access_token(identity=email, user_claims=admin(email),fresh=True),
                            'refresh_token': 
                            create_refresh_token(identity=email, user_claims=admin(email))
                            }
                        return make_response(jsonify(ret), 200)
                    elif (user_data['role']=="root"):
                        ret = {'access_token':
                         create_access_token(identity=email, user_claims=root(email),fresh=True),
                         'refresh_token': 
                         create_refresh_token(identity=email, user_claims=root(email))
                         }

                        return make_response(jsonify(ret), 200)
                    else: 
                        return make_response(jsonify("msg: Contact admin"), 403)

                else:
                    return make_response("msg: Incorrect Password", 403)
            else:
                return make_response("msg: Invalid email address", 403)

@freshlogin_ns.route('/')
class freshlogin(Resource):
    @freshlogin_ns.doc('Login')
    @freshlogin_ns.expect(login_model)
    @jwt_optional
    def post(self):
        current_user = get_jwt_identity()
        if current_user:
            return make_response(jsonify("Msg: You're logged in"), 200)
        else:
            email = login_ns.payload['email']
            password = login_ns.payload['password']
            r = requests.get(database_url+email)
            print(database_url+email)
            if r.status_code == 200:
                user_data = r.json()
                validate_password = bcrypt.check_password_hash(user_data['password'],password)
                if validate_password:
                    if (user_data['role']=="user"):
                        ret = {
                            'access_token':
                        create_access_token(identity=email, user_claims=regular_user(email),fresh=True),
                        }

                        return make_response(jsonify(ret), 200)
                    elif (user_data['role']=="admin"):
                        ret = {
                            'access_token': 
                            create_access_token(identity=email, user_claims=admin(email),fresh=True),
                            }

                        return make_response(jsonify(ret), 200)

                    elif (user_data['role']=="root"):
                        ret = {'access_token':
                         create_access_token(identity=email, user_claims=root(email),fresh=True),
                         }

                        return make_response(jsonify(ret), 200)
                    else: 
                        return make_response(jsonify("msg: Contact admin"), 403)

                else:
                    return make_response("msg: Incorrect Password", 403)
            else:
                return make_response("msg: Invalid email address", 403)



@logout_ns.route('/')
class logout(Resource):
    @logout_ns.doc('Logout: Revoke current users access tokens')
    @jwt_required
    def get(self):
        jti = get_raw_jwt()['jti']
        blacklist.add(jti)
        return make_response(jsonify({"msg": "Successfully logged out"}), 200)

    @logout_ns.doc('Logout: Revoke current users refresh tokens')
    @jwt_refresh_token_required
    def delete(self):
        jti = get_raw_jwt()['jti']
        blacklist.add(jti)
        return make_response(jsonify({"msg": "Successfully logged out"}), 200)


@refresh_ns.route('/')
class refresh(Resource):
    @refresh_ns.doc('Refresh tokens')
    @jwt_refresh_token_required
    def get(self):
        current_user = get_jwt_identity()

        ret = {
            'access_token': create_access_token(identity=current_user, user_claims=get_jwt_claims(),fresh=False)
        }
        return make_response(jsonify(ret), 200)

@register_ns.route('/')
class Register(Resource):
    @register_ns.doc('Register users')
    @register_ns.expect(users_model)
    def post(self):
        unvalidated_email = register_ns.payload['email']
        is_valid = validate_email(unvalidated_email)
        if is_valid:
            email = unvalidated_email
        else:
            return "Email address is not valid"
        username = register_ns.payload['name']
        password = register_ns.payload['password']
        role = register_ns.payload['role']
        r = requests.get(database_url+email)
        if(r.status_code==200):
            return jsonify("Error:Email already taken")
        else:
            password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
            data = {'name':username,'password':password_hash,'email':email,'role': role}
            rp = requests.post(url=database_url, json=data)
            email_data = {'subject': "Welcome",'to': email,'body': "You're a new user!!"}
            email_req = requests.post(url=email_url,json=email_data)
            result = rp.json()
            return result        
