from flask import Flask
from dotenv import load_dotenv
from datetime import timedelta

from connections.mysql_connections import connection
from models.user import User
import os 

from sqlalchemy.orm import sessionmaker
from sqlalchemy import select


load_dotenv



app = Flask(__name__)
app.config["SECRET_KEY"] =  os.getenv("SECRET_KEY")
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(minutes=5)

session = sessionmaker(connection)


@app.route("/")
def welcome():
    return {"Welcome to the web"}



@app.route("/onTerminal")
def get_dataTerminal():
    User_query = select(User)
    session = sessionmaker(connection)
    with session()as s:
        result = s.execute(User_query)
        for row in result.scalar():
            print(f"ID: {row.id}, Name: {row.username}, Email: {row.email}")
        return "succes print data on terminal"