# Анализатор банковских транзакций

## Установка
1. Установите Poetry (если не установлен)
2. Установите зависимости (poetry install)

## Использование

### Запуск основного приложения: 
poetry run python src/main.py

### Запуск тестов: 
poetry run pytest -v

## API Интеграция

Проект использует:
- [Exchangerate-API](https://www.exchangerate-api.com/) для курсов валют
- [Alpha Vantage](https://www.alphavantage.co/) для данных об акциях

Для работы необходимо задать ключи в `.env` файле.