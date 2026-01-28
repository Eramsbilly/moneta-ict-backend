from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import Investment, User, db

invest_bp = Blueprint("invest", __name__)

# 🇨🇴 Investment Plans (COP)
PLANS = [
    {"name": "Plan 1", "min": 50000, "daily": 8600, "days": 30},
    {"name": "Plan 2", "min": 100000, "daily": 17500, "days": 30},
    {"name": "Plan 3", "min": 200000, "daily": 36000, "days": 30},
    {"name": "Plan 4", "min": 300000, "daily": 54000, "days": 30},
    {"name": "Plan 5", "min": 500000, "daily": 90000, "days": 30},
]

@invest_bp.route("/plans")
def plans():
    return PLANS

@invest_bp.route("/buy", methods=["POST"])
@jwt_required()
def buy():
    uid = get_jwt_identity()
    data = request.json

    user = User.query.get(uid)
    if user.balance < data["amount"]:
        return {"error": "Insufficient balance"}, 400

    user.balance -= data["amount"]

    inv = Investment(
        user_id=uid,
        plan_name=data["plan"],
        amount=data["amount"],
        daily_return=data["daily"],
        days_left=data["days"]
    )

    db.session.add(inv)
    db.session.commit()
    return {"msg": "Investment activated"}
