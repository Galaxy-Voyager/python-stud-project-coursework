import logging
from typing import Dict

import pandas as pd


def filter_transactions_by_date(transactions: pd.DataFrame, start_date: str, end_date: str) -> pd.DataFrame:
    """
    Фильтрует транзакции по временному диапазону

    Args:
        transactions: DataFrame с транзакциями
        start_date: Начальная дата (YYYY-MM-DD)
        end_date: Конечная дата (YYYY-MM-DD)

    Returns:
        Отфильтрованный DataFrame
    """
    try:
        mask = (transactions["Дата операции"] >= pd.to_datetime(start_date)) & (
            transactions["Дата операции"] <= pd.to_datetime(end_date)
        )
        return transactions.loc[mask]
    except Exception as e:
        logging.error(f"Ошибка фильтрации по дате: {e}")
        return pd.DataFrame()


def calculate_category_stats(transactions: pd.DataFrame) -> Dict[str, float]:
    """
    Считает статистику по категориям расходов

    Args:
        transactions: DataFrame с транзакциями

    Returns:
        Словарь {категория: сумма}
    """
    try:
        expenses = transactions[transactions["Сумма платежа"] < 0]
        return expenses.groupby("Категория")["Сумма платежа"].sum().to_dict()
    except Exception as e:
        logging.error(f"Ошибка расчета статистики: {e}")
        return {}


def format_transaction_dates(transactions: pd.DataFrame) -> pd.DataFrame:
    """
    Конвертирует даты в строковый формат

    Args:
        transactions: Исходный DataFrame

    Returns:
        DataFrame с отформатированными датами
    """
    df = transactions.copy()
    df["Дата операции"] = df["Дата операции"].dt.strftime("%Y-%m-%d %H:%M:%S")
    return df
