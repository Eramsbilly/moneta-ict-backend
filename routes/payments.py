from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import Transaction, db
from flask import current_app

pay_bp = Blueprint("payments", __name__)

@pay_bp.route("/deposit", methods=["POST"])
@jwt_required()
def deposit():
    amount = request.json["amount"]
    if amount < current_app.config["MIN_DEPOSIT"]:
        return {"error": "Below minimum deposit"}, 400

    tx = Transaction(
        user_id=get_jwt_identity(),
        type="deposit",
        amount=amount
    )
    db.session.add(tx)
    db.session.commit()
    return {"msg": "Deposit pending admin approval"}

@pay_bp.route("/withdraw", methods=["POST"])
@jwt_required()
def withdraw():
    amount = request.json["amount"]
    if amount < current_app.config["MIN_WITHDRAW"]:
        return {"error": "Below minimum withdrawal"}, 400

    tx = Transaction(
        user_id=get_jwt_identity(),
        type="withdraw",
        amount=amount
    )
    db.session.add(tx)
    db.session.commit()
    return {"msg": "Withdrawal pending admin approval"}
