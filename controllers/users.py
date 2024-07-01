from flask import Blueprint, request

from connections.mysql_connections import connection
from sqlalchemy.orm import sessionmaker
from models.user import User
from sqlalchemy.exc import SQLAlchemyError
from flask_login import login_user, login_required, logout_user, current_user
from flask import jsonify, abort
from sqlalchemy import select


user_routes = Blueprint("user_routes", __name__)

@user_routes.route("/register", methods=["POST"])
# @swag_from("docs/register_newUser.yml")
def register_userData():
    Session = sessionmaker(connection)
    s = Session()
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
