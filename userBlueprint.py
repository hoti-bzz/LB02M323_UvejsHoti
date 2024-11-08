"""
UserBlueprint
"""
from flask import Blueprint, request, jsonify

user_blueprint = Blueprint('users', __name__)

# Global users list
users = []


@user_blueprint.route('/register', methods=['POST'])
def register_user():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    users.append({"username": username, "password": password})
    return jsonify({"message": f"User {username} successfully registered."})


@user_blueprint.route('/login', methods=['POST'])
def login_user():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    for user in users:
        if user["username"] == username and user["password"] == password:
            return jsonify({"message": f"Welcome back, {username}!"})
    return jsonify({"message": "Login failed. Please check your credentials."}), 401


@user_blueprint.route('/list', methods=['GET'])
def list_users():
    if not users:
        return jsonify({"message": "No users registered."})
    formatted_users = [
        {"username": u['username'], "password": u['password']} for u in users
    ]
    return jsonify(formatted_users)

