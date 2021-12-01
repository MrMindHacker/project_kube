from flask import Flask, request
from functools import wraps
from flask_sqlalchemy import SQLAlchemy
import jwt, datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///da1.sqlite"
app.config["JWT_SECRET_KEY"] = 't1NP63m4wnBg6nyHYKfmc2TpCOGI4nss'

db = SQLAlchemy(app)



class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    useremail = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)

db.create_all()

def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):

        token = None

        if 'x-access-tokens' in request.headers:
            token = request.headers['x-access-tokens']

        if not token:
            return {'message': 'a valid token is missing'}, 400

        try:
            data = jwt.decode(token, app.config["JWT_SECRET_KEY"], algorithms="HS256")
            current_user = User.query.filter_by(id=data['id']).first()
        except Exception as e:
            print(e)
            return {'message': 'token is invalid'}, 400

        return f(current_user, *args, **kwargs)
    return decorator

@app.route('/create', methods=['POST'])
def create():
    # print("called by: ", current_user)
    params = request.json
    u = User(username=params["username"], useremail=params["useremail"], password="sha256" + params["password"])
    db.session.add(u)
    db.session.commit()
    return {"Message": "Created successfully"}

@app.route('/login', methods=['POST'])
def login():
    params = request.json
    u = User.query.filter_by(username=params["username"]).first()

    if u == None or u.password != "sha256" + params["password"]:
        return {"Message": "Invalid credentials"}, 400

    expires = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
    # token = jwt.encode({'id': u.id, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY']) 
    access_token = jwt.encode({'id': u.id, 'exp' : expires}, app.config['JWT_SECRET_KEY'], algorithm="HS256")

    return {"Message": "Login successfull", "token": access_token}, 200

@app.route('/read', methods=['GET'])
@token_required
def read(current_user):
    users = User.query.all()
    # print(type(data))
    u = {}
    for user in users:
        u[user.id] = {"username": user.username, "useremail": user.useremail, "password": user.password}
    return u

@app.route('/update/<int:pk>', methods=[ 'PUT'])
@token_required
def update(current_user, pk):
    params = request.json
    print(current_user)

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

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)