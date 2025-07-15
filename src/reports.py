import logging
from datetime import datetime, timedelta
from typing import Dict, Optional

import pandas as pd


def spending_by_category(transactions: pd.DataFrame, category: str, date: Optional[str] = None) -> Dict:
    """
    Анализ трат по категории за последние 3 месяца

    Args:
        transactions: DataFrame с транзакциями
        category: Категория для анализа
        date: Опорная дата (если None - текущая дата)

    Returns:
        Словарь с результатами анализа
    """
    try:
        end_date = pd.to_datetime(date) if date else pd.to_datetime(datetime.now())
        start_date = end_date - timedelta(days=90)

        mask = (
            (transactions["Дата операции"] >= start_date)
            & (transactions["Дата операции"] <= end_date)
            & (transactions["Категория"] == category)
        )

        result = transactions[mask].groupby("Категория")["Сумма платежа"].agg(["sum", "count"])

        return {
            "category": category,
            "total": result["sum"].iloc[0],
            "count": result["count"].iloc[0],
            "period": f"{start_date.date()} - {end_date.date()}",
        }
    except Exception as e:
        logging.error(f"Ошибка анализа трат: {e}")
        return {}


def spending_by_weekday(transactions: pd.DataFrame, date: Optional[str] = None) -> Dict:
    """
    Анализ трат по дням недели за последние 3 месяца

    Args:
        transactions: DataFrame с транзакциями
        date: Опорная дата (если None - текущая дата)

    Returns:
        Словарь со средними тратами по дням недели
    """
    try:
        end_date = pd.to_datetime(date) if date else pd.to_datetime(datetime.now())
        start_date = end_date - timedelta(days=90)

        # Фильтрация по периоду
        period_trans = transactions[
            (transactions["Дата операции"] >= start_date) & (transactions["Дата операции"] <= end_date)
        ].copy()

        # Группировка по дням недели
        period_trans.loc[:, "day_of_week"] = period_trans["Дата операции"].dt.day_name()
        return period_trans.groupby("day_of_week")["Сумма платежа"].mean().to_dict()
    except Exception as e:
        logging.error(f"Ошибка анализа по дням недели: {e}")
        return {}
