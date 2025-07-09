import os
from unittest.mock import patch, MagicMock
import pytest
from src.config import API_KEYS


def test_api_keys_loading():
    # Тест с явной передачей переменных
    with patch.dict(os.environ, {
        "CURRENCY_API_KEY": "test_currency",
        "STOCK_API_KEY": "test_stock"
    }):
        # Мокаем load_dotenv чтобы он не перезаписывал наши переменные
        with patch("src.config.load_dotenv", return_value=None):
            from importlib import reload
            from src import config
            reload(config)

            assert config.API_KEYS["CURRENCY_API_KEY"] == "test_currency"
            assert config.API_KEYS["STOCK_API_KEY"] == "test_stock"


def test_missing_keys():
    # Полностью изолируем тест от реальных переменных
    with patch.dict(os.environ, {}, clear=True):
        # Мокаем load_dotenv чтобы он ничего не загружал
        with patch("src.config.load_dotenv") as mock_load:
            mock_load.return_value = None

            # Мокаем os.getenv чтобы возвращал None независимо от реального окружения
            with patch("os.getenv", return_value=None):
                from importlib import reload
                from src import config
                reload(config)

                assert config.API_KEYS["CURRENCY_API_KEY"] is None
                assert config.API_KEYS["STOCK_API_KEY"] is None
