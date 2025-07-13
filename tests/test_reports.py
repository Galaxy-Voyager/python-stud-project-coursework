from datetime import datetime, timedelta

import pandas as pd
import pytest

from src.reports import spending_by_category, spending_by_weekday


@pytest.fixture
def report_data():
    dates = [datetime.now() - timedelta(days=x) for x in range(100)]
    return pd.DataFrame(
        {
            "Дата операции": dates,
            "Сумма платежа": [-100 * (i % 5 + 1) for i in range(100)],
            "Категория": ["Еда" if i % 2 else "Транспорт" for i in range(100)],
        }
    )


def test_spending_by_category(report_data):
    result = spending_by_category(report_data, "Еда")
    assert result["category"] == "Еда"
    assert result["total"] < 0
    assert result["count"] > 0


def test_spending_by_weekday(report_data):
    result = spending_by_weekday(report_data)
    assert len(result) == 7  # 7 дней в неделе
    assert all(isinstance(v, float) for v in result.values())
