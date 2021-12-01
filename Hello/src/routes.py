from src.models import User
from src import app, api, db
from flask_restful import Resource, abort, reqparse
import datetime, jwt
from src.decorators import token_required

user_create_args = reqparse.RequestParser()
user_create_args.add_argument("username", type=str, required=True)
user_create_args.add_argument("useremail", type=str, required=True)
user_create_args.add_argument("password", type=str, required=True)

user_update_args = reqparse.RequestParser()
user_update_args.add_argument("username", type=str)
user_update_args.add_argument("useremail", type=str)
user_update_args.add_argument("password", type=str)

login_args = reqparse.RequestParser()
login_args.add_argument("username", type=str, required=True, help="Username Required")
login_args.add_argument("useremail", type=str, required=False)
login_args.add_argument("password", type=str, required=True, help="Password Required")


class create(Resource):
    def post(self):
        params = user_create_args.parse_args()
        u = User(username=params["username"], useremail=params["useremail"], password="sha256" + params["password"])
        db.session.add(u)
        db.session.commit()
        return {"Message": "Created successfully"}

class read(Resource):
    @token_required
    def get(self, data):
        users = User.query.all()
        print(type(data))
        u = {}
        for user in users:
            u[user.id] = {"username": user.username, "useremail": user.useremail, "password": user.password}
        return u

class update(Resource):
    @token_required
    def put(self, pk, data):
        print(pk)
        print(data)
        params = user_update_args.parse_args()

        u = User.query.filter_by(id=pk).first()

        if u == None:
            return {"Message": "Check your user id"}, 400

        if "username" in params:
            u.username = params["username"]
        elif "useremail" in params:
            u.useremail = params["useremail"]
        elif "password" in params:
            u.password = params["password"]

        db.session.add(u)
        db.session.commit()
        return {"Message": "Updated successfully"}

class delete(Resource):
    @token_required
    def delete(self, pk):
        u = User.query.filter_by(id=pk).first()

        if u == None:
            return {"Message": "Check your user id"}, 400

        db.session.delete(u)
        db.session.commit()
        return {"Message": "Deleted successfully"}, 204


class login(Resource):
    def post(self):
        params = login_args.parse_args()
        u = User.query.filter_by(username=params["username"]).first()

        if u == None or u.password != "sha256" + params["password"]:
            return {"Message": "Invalid credentials"}, 400

        expires = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        access_token = jwt.encode({'id': u.id, 'exp' : expires}, app.config['SECRET_KEY'], algorithm="HS256")

        return {"Message": "Login successfull", "token": access_token}, 200

api.add_resource(create, '/create')
api.add_resource(read, '/read')
api.add_resource(update, '/update/<int:pk>')
api.add_resource(delete, '/delete/<int:pk>')
api.add_resource(login, '/login')
