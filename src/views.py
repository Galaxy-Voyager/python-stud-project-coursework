import logging
from datetime import datetime
from typing import Dict, List

import pandas as pd
import requests

from src.config import API_KEYS
from src.data_loader import load_transactions


def home_page(target_date: str) -> Dict:
    """Генерирует JSON-данные для главной страницы."""
    try:
        transactions = load_transactions("data/operations.xlsx")
        greeting = _generate_greeting(target_date)
        cards_data = _process_cards(transactions, target_date)
        top_transactions = _get_top_transactions(transactions, target_date, n=5)
        currency_rates = _fetch_currency_rates()
        stock_prices = _fetch_stock_prices()
        print("Карты после обработки:", cards_data)  # временный вывод перед return

        return {
            "greeting": greeting,
            "cards": cards_data,
            "top_transactions": top_transactions,
            "currency_rates": currency_rates,
            "stock_prices": stock_prices,
        }
    except Exception as e:
        logging.error(f"Ошибка в home_page: {e}")
        raise


def _generate_greeting(target_date: str) -> str:
    """Определяет приветствие по времени."""
    time = datetime.strptime(target_date, "%Y-%m-%d %H:%M:%S").time()
    if 5 <= time.hour < 12:
        return "Доброе утро"
    elif 12 <= time.hour < 18:
        return "Добрый день"
    elif 18 <= time.hour < 23:
        return "Добрый вечер"
    return "Доброй ночи"


def _process_cards(transactions: pd.DataFrame, target_date: str) -> List[Dict]:
    """Считает общие траты и кешбэк по картам."""
    try:
        filtered = transactions[
            (transactions["Дата операции"] <= pd.to_datetime(target_date))
            & (transactions["Статус"] == "OK")
            & (transactions["Номер карты"].notna())
        ]

        cards = (
            filtered.groupby("Номер карты")
            .agg({"Сумма платежа": lambda x: abs(x.sum()), "Кэшбэк": "sum"})
            .reset_index()
        )

        return [
            {"last_digits": str(card)[-4:], "total_spent": round(total, 2), "cashback": round(cashback, 2)}
            for card, total, cashback in cards.itertuples(index=False)
        ]
    except Exception as e:
        logging.error(f"Ошибка в _process_cards: {e}")
        raise


def _get_top_transactions(transactions: pd.DataFrame, target_date: str, n: int = 5) -> List[Dict]:
    filtered = transactions[
        (transactions["Дата операции"] <= pd.to_datetime(target_date)) & (transactions["Сумма платежа"] < 0)
    ].nlargest(n, "Сумма платежа", keep="all")

    # Преобразуем Timestamp в строку
    result = filtered[["Дата операции", "Сумма платежа", "Категория", "Описание"]].to_dict("records")

    for item in result:
        item["Дата операции"] = item["Дата операции"].strftime("%Y-%m-%d %H:%M:%S")

    return result


def _fetch_currency_rates() -> List[Dict]:
    """Получает актуальные курсы валют через API"""
    try:
        if not API_KEYS.get("CURRENCY_API_KEY"):
            raise ValueError("Не задан API ключ для курсов валют")

        response = requests.get(
            "https://api.exchangerate-api.com/v4/latest/RUB",
            params={"access_key": API_KEYS["CURRENCY_API_KEY"]},
            timeout=5,
        )
        response.raise_for_status()
        data = response.json()

        return [
            {"currency": "USD", "rate": round(1 / data["rates"]["USD"], 2)},
            {"currency": "EUR", "rate": round(1 / data["rates"]["EUR"], 2)},
        ]
    except Exception as e:
        logging.error(f"Ошибка получения курсов валют: {str(e)}")
        return []  # Возвращаем пустой список при ошибке


def _fetch_stock_prices() -> List[Dict]:
    """Получает цены акций через Alpha Vantage API"""
    try:
        stocks = ["AAPL", "MSFT", "GOOGL"]  # Примеры тикеров
        prices = []

        for stock in stocks:
            response = requests.get(
                "https://www.alphavantage.co/query",
                params={"function": "GLOBAL_QUOTE", "symbol": stock, "apikey": API_KEYS["STOCK_API_KEY"]},
            )
            data = response.json()
            prices.append({"stock": stock, "price": float(data["Global Quote"]["05. price"])})

        return prices
    except Exception as e:
        logging.error(f"Ошибка получения цен акций: {e}")
        return []
