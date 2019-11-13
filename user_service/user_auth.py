from user_manager import User, Username, app, bcrypt, fields, api, Namespace, Resource

ns1 = Namespace('login')
api.add_namespace(ns1)
login_model = ns1.model('Login Details',{
    'email': fields.String(required=True),
    'password': fields.String(required=True)
})


@ns1.route('/')
class Login(Resource):
    @ns1.doc('Login')
    @ns1.expect(login_model)
    def post(self):
        email = ns1.payload['email']
        password = ns1.payload['password']
        email_finder = db_users.find_one({'email':email})
        if email_finder:
            validate_password = bcrypt.check_password_hash(email_finder['password'],password)
            if validate_password:
                return "User logged in"
            else:
                return "Incorrect Password"
        else:
            return "Email not found"



