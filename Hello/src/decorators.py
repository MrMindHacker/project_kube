import jwt
from flask import request
from functools import wraps
from src import app
from src.models import User



def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):

            token = None

            if 'x-access-tokens' in request.headers:
                token = request.headers['x-access-tokens']

            if not token:
                return {'message': 'a valid token is missing'}, 400

            try:
                data = jwt.decode(token, app.config["SECRET_KEY"], algorithms="HS256")
                current_user = User.query.filter_by(id=data['id']).first()
            except Exception as e:
                print(e)
                return {'message': 'token is invalid'}, 400

            return f(current_user, *args, **kwargs)
    return decorator