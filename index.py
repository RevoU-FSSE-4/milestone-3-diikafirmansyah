from flask import Flask, jsonify
from dotenv import load_dotenv
from datetime import timedelta

from connectors.mysql_connector import connection
from models.user import User
# from models.account import Account
import os 
from controllers.users import users_routes
from controllers.accounts import accounts_routes
from models.blocklist import BLOCKLIST

from sqlalchemy.orm import sessionmaker
from sqlalchemy import select

from flask_jwt_extended import JWTManager


load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(minutes=10)
jwt = JWTManager(app)

app.register_blueprint(users_routes)
app.register_blueprint(accounts_routes)

Session = sessionmaker(connection)


@jwt.token_in_blocklist_loader
def check_if_token_in_blocklist(jwt_header, jwt_payload):
    return jwt_payload["jti"] in BLOCKLIST


@jwt.revoked_token_loader
def revoked_token_callback(jwt_header, jwt_payload):
    return (
        jsonify(
            {"description": "The token has been revoked.", "error": "token_revoked"}
        ),
        401,
    )


@app.route("/")
def welcome():
    return "Welcome to the web"


@app.route("/onTerminal", methods=["GET"])
def get_dataTerminal():
    user_query = select(User)
    Session = sessionmaker(connection)
    with Session()as s:
        result = s.execute(user_query)
        for row in result.scalars():
            print(f"ID: {row.id}, Name: {row.username}, Email: {row.email}")
    
    Session().commit()
    return "Success Print Data on Terminal"
