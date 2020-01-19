from user_auth import *

@ns.route('/')
class User(Resource):    
    @ns.doc('List all users')
    @admin_required
    def get(self):
        r = requests.get(database_url)
        user_data = r.json()
        return jsonify(user_data)
    
@ns.route('/<email>')
@ns.param('email','User email id')
@ns.response(404,'User not found')
class Username(Resource):
    @ns.doc('List the particular user given the email id')
    @jwt_required
    def get(self, email):
        url = database_url+email
        r = requests.get(url = url)
        result = r.json()
        return result

    @ns.doc('Deletes a user by taking a username as input')
    @fresh_jwt_required
    def delete(self,email):
        url = database_url+email
        r = requests.get(url = url)
        result = r.json()
        return result
    
