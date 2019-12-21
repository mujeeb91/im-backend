from datetime import datetime, timedelta
from flask import Blueprint, current_app as app, jsonify, request, Response
from flask_api import status
import jwt
from jwt.exceptions import ExpiredSignatureError
from functools import wraps

from .model import User, check_password_hash

auth = Blueprint('auth', __name__)


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization', '').replace('Token ', '')
        if not token:
            return jsonify({'message': 'Token is missing'}), status.HTTP_403_FORBIDDEN
        try:
            jwt.decode(token, app.config['SECRET_KEY'])
        except ExpiredSignatureError:
            return jsonify({'message': 'Token is invalid'}), status.HTTP_403_FORBIDDEN
        return f(*args, **kwargs)
    return decorated


@auth.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')
    user = User.query.filter_by(username=username).first()
    if user and check_password_hash(user.password, password):
        token = jwt.encode(
            {
                'username': username,
                'exp': datetime.utcnow() + timedelta(minutes=10)
            },
            app.config['SECRET_KEY']
        )
        return jsonify({'token': token.decode('UTF-8')}), status.HTTP_200_OK
    return jsonify({'message': 'Invalid credentials'}), status.HTTP_401_UNAUTHORIZED

