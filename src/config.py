import os

from dotenv import load_dotenv


def load_config():
    """Загружает конфигурацию из переменных окружения"""
    load_dotenv()  # Загружает переменные из .env

    return {"CURRENCY_API_KEY": os.getenv("CURRENCY_API_KEY"), "STOCK_API_KEY": os.getenv("STOCK_API_KEY")}


API_KEYS = load_config()
