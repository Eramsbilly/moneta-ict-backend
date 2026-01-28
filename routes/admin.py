from flask import Blueprint, request, current_app
from models import User, Transaction, db
import requests

admin_bp = Blueprint("admin", __name__)

def notify_telegram(message):
    token = current_app.config["BOT_TOKEN"]
    chat_id = current_app.config["CHAT_ID"]
    if not token or not chat_id:
        return
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    requests.post(url, json={
        "chat_id": chat_id,
        "text": message
    })

@admin_bp.route("/users")
def users():
    return [
        {"id": u.id, "email": u.email, "balance": u.balance}
        for u in User.query.all()
    ]

@admin_bp.route("/approve", methods=["POST"])
def approve():
    tx = Transaction.query.get(request.json["tx_id"])
    if not tx:
        return {"error": "Transaction not found"}, 404

    tx.status = "approved"
    user = User.query.get(tx.user_id)

    if tx.type == "deposit":
        user.balance += tx.amount

    db.session.commit()

    notify_telegram(
        f"✅ APPROVED\n"
        f"User: {user.email}\n"
        f"Type: {tx.type}\n"
        f"Amount: {tx.amount} COP"
    )

    return {"msg": "Transaction approved"}
