import logging
from typing import Dict, List

import pandas as pd


def find_transactions_by_description(transactions: pd.DataFrame, search_query: str) -> List[Dict]:
    """
    Поиск транзакций по описанию

    Args:
        transactions: DataFrame с транзакциями
        search_query: Строка для поиска

    Returns:
        Список найденных транзакций
    """
    try:
        mask = transactions["Описание"].str.contains(search_query, case=False, na=False)
        return transactions[mask].to_dict("records")
    except Exception as e:
        logging.error(f"Ошибка поиска транзакций: {e}")
        return []


def find_phone_transactions(transactions: pd.DataFrame) -> List[Dict]:
    """
    Поиск транзакций с телефонными номерами в описании

    Args:
        transactions: DataFrame с транзакциями

    Returns:
        Список транзакций с телефонами
    """
    phone_regex = r"(?:\+7|8)[\s\-]?(?:\d{3})[\s\-]?\d{3}[\s\-]?\d{2}[\s\-]?\d{2}"
    try:
        mask = transactions["Описание"].str.contains(phone_regex, na=False)
        return transactions[mask].to_dict("records")
    except Exception as e:
        logging.error(f"Ошибка поиска телефонных номеров: {e}")
        return []


def calculate_investment(transactions: pd.DataFrame, round_limit: int = 10) -> float:
    """
    Расчет суммы для инвесткопилки через округление

    Args:
        transactions: DataFrame с транзакциями
        round_limit: Шаг округления (10, 50, 100)

    Returns:
        Сумма для инвесткопилки
    """
    try:
        rounded = (transactions["Сумма платежа"] / round_limit).abs().round() * round_limit
        return (rounded - transactions["Сумма платежа"].abs()).sum()
    except Exception as e:
        logging.error(f"Ошибка расчета инвесткопилки: {e}")
        return 0.0
