from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config import Config
from models import db

from routes.auth import auth_bp
from routes.user import user_bp
from routes.investment import invest_bp
from routes.payments import pay_bp
from routes.admin import admin_bp

app = Flask(__name__)
app.config.from_object(Config)

CORS(app)
db.init_app(app)
JWTManager(app)

@app.route("/api/ping")
def ping():
    return jsonify({
        "ok": True,
        "app": "MONETA-ICT",
        "country": "CO",
        "currency": "COP"
    })

app.register_blueprint(auth_bp, url_prefix="/api/auth")
app.register_blueprint(user_bp, url_prefix="/api/user")
app.register_blueprint(invest_bp, url_prefix="/api/invest")
app.register_blueprint(pay_bp, url_prefix="/api/payments")
app.register_blueprint(admin_bp, url_prefix="/api/admin")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run()
