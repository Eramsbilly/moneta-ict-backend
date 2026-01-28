from flask import Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import User

user_bp = Blueprint("user", __name__)

@user_bp.route("/me")
@jwt_required()
def me():
    user = User.query.get(get_jwt_identity())
    return {
        "email": user.email,
        "balance": user.balance
    }
