from user_manager import User, Username, app, bcrypt, fields, api, Namespace, Resource

login_ns = Namespace('login')
register_ns = Namespace('register')
api.add_namespace(login_ns)
login_model = login_ns.model('Login Details',{
    'email': fields.String(required=True),
    'password': fields.String(required=True)
})


@login_ns.route('/')
class Login(Resource):
    @login_ns.doc('Login')
    @login_ns.expect(login_model)
    def post(self):
        email = login_ns.payload['email']
        password = login_ns.payload['password']
        email_finder = db_users.find_one({'email':email})
        if email_finder:
            validate_password = bcrypt.check_password_hash(email_finder['password'],password)
            if validate_password:
                return "User logged in"
            else:
                return "Incorrect Password"
        else:
            return "Email not found"



