from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from ..models import db, User

user_bp = Blueprint('users', __name__)

@user_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data['username']
    password = data['password']

    if User.query.filter_by(username=username).first():
        return jsonify({"message": "Username already exists"}), 400

    user = User(username=username)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201

@user_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data['username']
    password = data['password']

    user = User.query.filter_by(username=username).first()
    if not user or not user.check_password(password):
        return jsonify({"message": "Invalid username or password"}), 401

    # ✅ Use user.id or username as identity
    access_token = create_access_token(identity=str(user.id))


    return jsonify({
        "access_token": access_token,
        "message": "Login successful"
    }), 200
