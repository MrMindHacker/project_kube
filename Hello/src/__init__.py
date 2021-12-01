from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
app = Flask(__name__)
api = Api(app)
app.config['SECRET_KEY']='Th1s1ss3cr3t'
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///da.sqlite"
app.config["JWT_SECRET_KEY"] = 't1NP63m4wnBg6nyHYKfmc2TpCOGI4nss'
app.config["SALT"] = 'SomeSalt'
db = SQLAlchemy(app)


from . import models, routes

# db.create_all()

# u = models.User(username="username", useremail="useremail", password="password")
# db.session.add(u)
# db.session.commit()