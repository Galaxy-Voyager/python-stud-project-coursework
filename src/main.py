import json
from datetime import datetime

from src.views import home_page


def convert_to_serializable(obj):
    """Конвертирует объекты для JSON-сериализации"""
    if isinstance(obj, (datetime, pd.Timestamp)):
        return obj.strftime("%Y-%m-%d %H:%M:%S")
    raise TypeError(f"Object of type {type(obj).__name__} is not JSON serializable")


def main():
    try:
        result = home_page("2021-12-31 12:00:00")
        print(json.dumps(result, indent=2, ensure_ascii=False, default=convert_to_serializable))
    except Exception as e:
        print(f"Ошибка при выполнении: {e}")


if __name__ == "__main__":
    import pandas as pd  # Добавляем импорт pandas

    main()
