import json
import sys
from pathlib import Path


sys.path.append(str(Path(__file__).parent.parent))


from src.data_loader import load_transactions
from src.views import home_page


def main():
    """Основная функция запуска приложения"""
    try:
        # Пример использования
        result = home_page("2023-01-01 12:00:00")
        print(json.dumps(result, indent=2, ensure_ascii=False, default=str))  # Конвертирует datetime в строки

    except Exception as e:
        print(f"Ошибка при выполнении: {str(e)}")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
