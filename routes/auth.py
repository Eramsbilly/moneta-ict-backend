from flask import Blueprint, request
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from models import User, db
from flask import current_app

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.json

    if User.query.filter_by(email=data["email"]).first():
        return {"error": "Email already registered"}, 400

    user = User(
        email=data["email"],
        password=generate_password_hash(data["password"]),
        balance=current_app.config["WELCOME_BONUS"]
    )
    db.session.add(user)
    db.session.commit()
    return {"msg": "Registered successfully"}

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    user = User.query.filter_by(email=data["email"]).first()

    if not user or not check_password_hash(user.password, data["password"]):
        return {"error": "Invalid credentials"}, 401

    token = create_access_token(identity=user.id)
    return {"token": token}
