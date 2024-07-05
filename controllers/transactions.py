from flask import Blueprint, request, jsonify

from connectors.mysql_connector import connection
from models.transaction import Transaction

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


transactions_routes = Blueprint("transactions_routes", __name__)
Session = sessionmaker(connection)
s = Session()


@transactions_routes.route("/transactions", methods=['GET'])
def getAll_transaction():
    try:
        transaction_query = select(Transaction)

        search_keyword = request.args.get("query")
        if search_keyword is not None:
            transaction_query = transaction_query.where(
                Transaction.from_account_id.like(f"%{search_keyword}%")
            )

        result = s.execute(transaction_query)
        transactions = []

        for row in result.scalars():
            transactions.append(
                {
                    "id": row.id,
                    "from_account_id": row.from_account_id,
                    "to_account_id": row.to_account_id,
                    "amount": row.amount,
                    "type": row.type,
                }
            )

        return {"Accounts": transactions}, 200

    except Exception as e:
        print(e)
        s.rollback()
        return {"message": "Unexpected Error"}, 500


@transactions_routes.route("/transactions/<id>", methods=["GET"])
@jwt_required()
def get_transactions_by_id(id):
    try:
        transactions = s.query(Transaction).filter(Transaction.id == id).all()

        if not transactions:
            return jsonify({"message": "No transaction found for this user"}), 404

        transactions_list = []
        for transaction in transactions:
            account_details = {
                "id": transaction.id,
                "from_account_id": transaction.from_account_id,
                "to_account_id": transaction.to_account_id,
                "amount": transaction.amount,
                "type": transaction.type,
            }
            transactions_list.append(account_details)

        return jsonify({"accounts": transactions_list}), 200

    except Exception as e:
        print(e)
        s.rollback()
        return jsonify({"message": "Unexpected Error"}), 500


from flask import request, jsonify


@transactions_routes.route("/transactions", methods=["POST"])
# @jwt_required()
def create_transaction():
    try:
        # Extracting data from request form
        from_account_id = request.form.get("from_account_id")
        to_account_id = request.form.get("to_account_id")
        amount = request.form.get("amount")
        transaction_type = request.form.get("type")
        description = request.form.get("description")

        if not all([from_account_id, to_account_id, amount, transaction_type]):
            return {"message": "Missing required fields"}, 400

        # Convert amount to decimal if needed
        amount = float(amount)  # Assuming amount is in string format from form data

        if transaction_type == "deposit":
            # Deposit: Add amount to 'to_account_id'
            new_transaction = Transaction(
                to_account_id=to_account_id,
                amount=amount,
                type="deposit",
                description=description,
            )

            # Perform additional actions for deposit (e.g., add amount to account)

        elif transaction_type == "transfer":
            # Transfer: Subtract amount from 'from_account_id' and add to 'to_account_id'
            new_transaction = Transaction(
                from_account_id=from_account_id,
                to_account_id=to_account_id,
                amount=amount,
                type="transfer",
                description=description,
            )

            # Perform additional actions for transfer (e.g., subtract amount from sender account)

        elif transaction_type == "withdraw":
            # Withdraw: Subtract amount from 'from_account_id'
            new_transaction = Transaction(
                from_account_id=from_account_id,
                amount=amount,
                type="withdraw",
                description=description,
            )

            # Perform additional actions for withdraw (e.g., subtract amount from account)

        else:
            return {"message": "Invalid transaction type"}, 400

        s.add(new_transaction)
        s.commit()

        return {"message": "Transaction created successfully"}, 201

    except Exception as e:
        print(e)
        s.rollback()
        return {"message": "Unexpected Error"}, 500