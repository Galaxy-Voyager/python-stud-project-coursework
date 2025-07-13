import pandas as pd
import pytest

from src.services import calculate_investment, find_phone_transactions, find_transactions_by_description


@pytest.fixture
def sample_transactions():
    return pd.DataFrame(
        {
            "Описание": ["Покупка в Магните +7 999 123-45-67", "Оплата курсов", "Перевод на карту 89161234567"],
            "Сумма платежа": [-1000, -5000, -200],
            "Категория": ["Супермаркеты", "Образование", "Переводы"],
        }
    )


def test_find_transactions_by_description(sample_transactions):
    result = find_transactions_by_description(sample_transactions, "магнит")
    assert len(result) == 1
    assert result[0]["Категория"] == "Супермаркеты"


def test_find_phone_transactions(sample_transactions):
    result = find_phone_transactions(sample_transactions)
    assert len(result) == 2
    assert all("+7" in t["Описание"] or "8916" in t["Описание"] for t in result)


def test_calculate_investment(sample_transactions):
    result = calculate_investment(sample_transactions, 10)
    assert isinstance(result, float)
