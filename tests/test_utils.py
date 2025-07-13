import pandas as pd
import pytest

from src.utils import calculate_category_stats, filter_transactions_by_date, format_transaction_dates


@pytest.fixture
def sample_transactions():
    return pd.DataFrame(
        {
            "Дата операции": pd.to_datetime(["2023-01-01", "2023-01-15", "2023-02-01"]),
            "Сумма платежа": [-1000, -500, 2000],
            "Категория": ["Еда", "Транспорт", "Зарплата"],
        }
    )


def test_filter_transactions_by_date(sample_transactions):
    filtered = filter_transactions_by_date(sample_transactions, "2023-01-01", "2023-01-31")
    assert len(filtered) == 2
    assert all(filtered["Дата операции"].dt.month == 1)


def test_calculate_category_stats(sample_transactions):
    stats = calculate_category_stats(sample_transactions)
    assert stats == {"Еда": -1000, "Транспорт": -500}
    assert "Зарплата" not in stats


def test_format_transaction_dates(sample_transactions):
    formatted = format_transaction_dates(sample_transactions)
    assert isinstance(formatted["Дата операции"].iloc[0], str)
    assert formatted["Дата операции"].iloc[0] == "2023-01-01 00:00:00"
