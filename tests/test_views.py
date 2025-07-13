from unittest.mock import MagicMock, patch

import pandas as pd
import pytest

from src.views import _generate_greeting, home_page


@pytest.mark.parametrize(
    "time,expected",
    [
        ("04:00:00", "Доброй ночи"),
        ("08:00:00", "Доброе утро"),
        ("14:00:00", "Добрый день"),
        ("20:00:00", "Добрый вечер"),
        ("23:59:59", "Доброй ночи"),
    ],
)
def test_generate_greeting(time, expected):
    date_str = f"2023-01-01 {time}"
    assert _generate_greeting(date_str) == expected


@pytest.fixture
def sample_data():
    """Фикстура с тестовыми данными, соответствующими реальной структуре"""
    return pd.DataFrame(
        {
            "Дата операции": pd.to_datetime(["2021-12-31 16:44:00", "2021-12-31 16:42:04", "2021-12-30 10:00:00"]),
            "Статус": ["OK", "OK", "OK"],
            "Номер карты": ["4556", "5091", "7197"],  # Уникальные номера карт
            "Сумма платежа": [-1000.0, -500.0, -300.0],
            "Кэшбэк": [10.0, 5.0, 0.0],
            "Категория": ["Супермаркеты", "АЗС", "Рестораны"],
            "Описание": ["Покупка в Магните", "Заправка", "Ужин"],
        }
    )


def test_home_page(sample_data, monkeypatch):
    monkeypatch.setattr("src.data_loader.load_transactions", lambda _: sample_data)
    result = home_page("2021-12-31 23:59:59")

    assert "greeting" in result
    assert isinstance(result["cards"], list)
    assert all("last_digits" in card for card in result["cards"])
    assert all(isinstance(card["total_spent"], float) for card in result["cards"])


@patch("requests.get")
def test_fetch_currency_rates(mock_get):
    # Настраиваем мок-ответ
    mock_response = MagicMock()
    mock_response.json.return_value = {"rates": {"USD": 0.013, "EUR": 0.011}, "base": "RUB"}
    mock_get.return_value = mock_response

    # Тестируем с подмененным API-ключом
    with patch.dict("src.config.API_KEYS", {"CURRENCY_API_KEY": "test_key"}):
        from src.views import _fetch_currency_rates

        result = _fetch_currency_rates()

        assert len(result) == 2
        assert result[0]["currency"] == "USD"
        assert isinstance(result[0]["rate"], float)
        assert result[1]["currency"] == "EUR"


def test_fetch_stock_prices():
    from src.views import _fetch_stock_prices

    result = _fetch_stock_prices()
    assert isinstance(result, list)
    assert all("stock" in item and "price" in item for item in result)


@patch("requests.get")
def test_fetch_currency_rates_error(mock_get):
    mock_get.side_effect = Exception("API error")
    with patch.dict("src.config.API_KEYS", {"CURRENCY_API_KEY": "test_key"}):
        from src.views import _fetch_currency_rates

        result = _fetch_currency_rates()
        assert result == []
