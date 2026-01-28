import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "CHANGE_ME")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", SECRET_KEY)

    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL", "sqlite:///moneta.db"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # 🇨🇴 Colombia localization
    COUNTRY = "CO"
    CURRENCY = "COP"
    MIN_DEPOSIT = 40000
    MIN_WITHDRAW = 25000
    WELCOME_BONUS = 12000

    # 🤖 Telegram
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    CHAT_ID = os.getenv("CHAT_ID")
    GROUP_LINK = os.getenv("GROUP_LINK")
