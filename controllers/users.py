from flask import Blueprint, request, jsonify, abort

from connectors.mysql_connector import connection
from models.user import User
from models.blocklist import BLOCKLIST


from sqlalchemy.orm import sessionmaker
from sqlalchemy import func
from datetime import datetime
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt_identity,
    get_jwt,
)
from models.blocklist import BLOCKLIST


users_routes = Blueprint("users_routes", __name__)
Session = sessionmaker(connection)
s = Session()


@users_routes.route("/register", methods=["POST"])
def register_usersData():
    s.begin()
    try:
        NewUser = User(
            username=request.form["username"],
            email=request.form["email"],
        )
        NewUser.set_password(request.form["password"])
        s.add(NewUser)
        s.commit()
    except Exception as e:
        print(e)
        s.rollback()
        return {"message": "Fail to Register New User"}, 500
    return {"message": "Success to Create New User"}, 200


@users_routes.route("/login", methods=["POST"])
def login_userData():
    try:
        email = request.form["email"]
        user = s.query(User).filter(User.email == email).first()

        if user == None:
            return {"message": "User not found"}, 403

        if not user.check_password(request.form["password"]):
            return {"message": "Invalid password"}, 403

        acces_token = create_access_token(
            identity=user.id, additional_claims={"email": user.email, "id": user.id}
        )
        s.flush()
        return {"access_tokern": acces_token, "message": "Success to Login user"}, 200
    except Exception as e:
        print(e)
        s.rollback()
        return {"message": "Failed to Login User"}, 500


@users_routes.route("/users/me", methods=["PUT"])
@jwt_required()
def update_current_user():
    current_user_id = get_jwt_identity()
    print(current_user_id)
    try:
        user = s.query(User).filter(User.id == current_user_id).first()
        if not user:
            return {"message": "User not found"}, 404

        if "username" in request.form:
            user.username = request.form["username"]
        if "email" in request.form:
            user.email = request.form["email"]

        user.update_at = datetime.now()

        s.add(user)
        s.commit()
        return {"message": "User updated successfully"}, 200

    except Exception as e:
        print(e)
        s.rollback()
        return {"message": "Failed to update user"}, 500


@users_routes.route("/users/me", methods=["GET"])
@jwt_required()
def get_current_user():
    current_user_id = get_jwt_identity()
    try:
        user = s.query(User).filter(User.id == current_user_id).first()
        if not user:
            return {"message": "User not found"}, 404

        user_data = {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "created_at": user.created_at,
            "update_at": user.update_at,
        }

        return jsonify(user_data), 200

    except Exception as e:
        print(e)
        return {"message": "Failed to retrieve user information"}, 500


@users_routes.route("/logout", methods=["POST"])
@jwt_required()
def logout():
    try:
        jti = get_jwt()["jti"]
        BLOCKLIST.add(jti)
        return jsonify({"message": "User successfully logged out"}), 200
    except Exception as e:
        print(e)
        return jsonify({"message": "Failed to logout"}), 500
