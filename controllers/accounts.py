from flask import Blueprint, request, jsonify

from connectors.mysql_connector import connection
from models.account import Account

from sqlalchemy.orm import sessionmaker
from sqlalchemy import select
from datetime import datetime
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt_identity,
    unset_jwt_cookies,
    get_jwt,
)

accounts_routes = Blueprint("accounts_routes", __name__)
Session = sessionmaker(connection)
s = Session()


@accounts_routes.route("/accounts", methods=["GET"])
def get_allAccount():
    try:
        Session = sessionmaker(bind=connection)
        with Session() as s:
            account_query = select(Account)

            search_keyword = request.args.get("query")
            if search_keyword is not None:
                account_query = account_query.where(
                    Account.account_number.like(f"%{search_keyword}%")
                )

            result = s.execute(account_query)
            accounts = []

            for row in result.scalars():
                accounts.append(
                    {
                        "id": row.id,
                        "user_id": row.user_id,
                        "account_type": row.account_type,
                        "account_number": row.account_number,
                        "balance": row.balance,
                    }
                )

            return (
                jsonify({"Accounts": accounts}),
                200,
            )

    except Exception as e:
        print(e)
        s.rollback()
        return jsonify({"message": "Unexpected Error"}), 500


@accounts_routes.route("/accounts/<user_id>", methods=["GET"])
@jwt_required()
def get_accounts_by_user_id(user_id):
    try:
        accounts = s.query(Account).filter(Account.user_id == user_id).all()

        if not accounts:
            return jsonify({"message": "No accounts found for this user"}), 404

        accounts_list = []
        for account in accounts:
            account_details = {
                "id": account.id,
                "user_id": account.user_id,
                "account_type": account.account_type,
                "account_number": account.account_number,
                "balance": account.balance,
            }
            accounts_list.append(account_details)

        return jsonify({"accounts": accounts_list}), 200

    except Exception as e:
        print(e)
        s.rollback()
        return jsonify({"message": "Unexpected Error"}), 500


@accounts_routes.route("/accounts/register", methods=["POST"])
def register_account():
    s.begin
    try:
        NewAccount = Account(
            user_id=request.form["users_id"],
            account_type=request.form["account_type"],
            account_number=request.form["account_number"],
            balance=request.form["balance"],
        )
        s.add(NewAccount)
        s.commit()
    except Exception as e:
        print(e)
        s.rollback()
        return {"message": "Unexpected Error"}, 500
    return {"message": "Account created successfully"}, 200


@accounts_routes.route("/accounts/<int:id>", methods=["PUT"])
@jwt_required()
def update_account(id):
    try:
        account = s.query(Account).filter(Account.id == id).first()

        if not account:
            return jsonify({"message": "Account not found"}), 404

        if "account_type" in request.form:
            account.account_type = request.form["account_type"]
        if "account_number" in request.form:
            account.account_number = request.form["account_number"]
        if "balance" in request.form:
            account.balance = request.form["balance"]

        s.commit()

    except Exception as e:
        print(e)
        s.rollback()
        return jsonify({"message": "Unexpected Error"}), 500

    return jsonify({"message": "Account updated successfully"}), 200


@accounts_routes.route("/accounts/<id>", methods=["DELETE"])
@jwt_required()
def delete_account_by_id(id):
    try:
        accounts = s.query(Account).filter(Account.id == id).all()

        if not accounts:
            return jsonify({"message": "No accounts found for this user"}), 404

        for account in accounts:
            s.delete(account)

        s.commit()

        return jsonify({"message": "Accounts deleted successfully"}), 200

    except Exception as e:
        print(e)
        s.rollback()
        return jsonify({"message": "Unexpected Error"}), 500
