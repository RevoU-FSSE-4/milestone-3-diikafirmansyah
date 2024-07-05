from flask import Blueprint, request, jsonify

from connectors.mysql_connector import connection
from models.transaction import Transaction
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
from sqlalchemy.orm.exc import NoResultFound


transactions_routes = Blueprint("transactions_routes", __name__)
Session = sessionmaker(connection)
s = Session()

@transactions_routes.route("/transactions", methods=["GET"])
def getAll_transaction():
    try:
        s = Session()
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

        return jsonify({"Transactions": transactions}), 200

    except Exception as e:
        print(e)
        s.rollback()
        return jsonify({"message": "Unexpected Error"}), 500


@transactions_routes.route("/transactions/<id>", methods=["GET"])
# @jwt_required()
def get_transactions_by_id(id):
    try:
        s = Session()
        transaction = s.query(Transaction).filter(Transaction.id == id).first()

        if not transaction:
            return jsonify({"message": "No transaction found for this user"}), 404

        # Ubah format respons untuk satu transaksi
        transaction_details = {
            "id": transaction.id,
            "from_account_id": transaction.from_account_id,
            "to_account_id": transaction.to_account_id,
            "amount": transaction.amount,
            "type": transaction.type,
        }

        return jsonify({"transaction": transaction_details}), 200

    except Exception as e:
        print(e)
        s.rollback()
        return jsonify({"message": "Unexpected Error"}), 500


@transactions_routes.route("/transaction/deposit", methods=["POST"])
# @login_required
def create_transaction_deposit():
    Session = sessionmaker(connection)
    session = Session()

    try:
        from_account_id = request.form.get("from_account_id")
        to_account_id = request.form.get("to_account_id")
        amount = request.form.get("amount")

        if not to_account_id or not amount:
            raise ValueError("Please fill in 'to_account_id' and 'amount'")

        new_deposit_transaction = Transaction(
            from_account_id=from_account_id,
            to_account_id=to_account_id,
            amount=amount,
            type="deposit",
            description="sending funds",
        )

        session.add(new_deposit_transaction)
        session.commit()

        return {"message": "succes"}, 200

    except Exception as e:
        return (
            jsonify(
                {"error": "Failed to make a deposit transaction", "message": str(e)}
            ),
            500,
        )

    finally:
        session.close()


@transactions_routes.route("/transaction/withdrawal", methods=["POST"])
# @login_required
def create_transaction_withdrawal():
    Session = sessionmaker(connection)
    session = Session()

    try:
        from_account_id = request.form.get("from_account_id")
        to_account_id = request.form.get("to_account_id")
        amount = request.form.get("amount")

        if not from_account_id or not amount:
            raise ValueError("Please fill in 'from_account_id' and 'amount'")

        new_withdrawal_transaction = Transaction(
            from_account_id=from_account_id,
            to_account_id=to_account_id,
            amount=amount,
            type="withdrawal",
            description="withdrawing funds",
        )

        session.add(new_withdrawal_transaction)
        session.commit()

        return {"message": "success"}, 200

    except Exception as e:
        return (
            jsonify(
                {"error": "Failed to make a withdrawal transaction", "message": str(e)}
            ),
            500,
        )

    finally:
        session.close()