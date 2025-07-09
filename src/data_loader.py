import pandas as pd


def load_transactions(filepath: str) -> pd.DataFrame:
    """
    Загружает и предобрабатывает транзакции из Excel-файла.

    Args:
        filepath: Путь к файлу operations.xlsx

    Returns:
        pd.DataFrame: Обработанный DataFrame с транзакциями

    Raises:
        FileNotFoundError: Если файл не существует
        ValueError: Если некорректный формат данных
    """
    df = pd.read_excel(filepath)

    # Конвертируем даты (учитываем формат день.месяц.год час:мин:сек)
    df["Дата операции"] = pd.to_datetime(df["Дата операции"], dayfirst=True)
    df["Дата платежа"] = pd.to_datetime(df["Дата платежа"], dayfirst=True)

    # Обработка номера карты (оставляем последние 4 цифры)
    df["Номер карты"] = df["Номер карты"].str.extract(r"\*(\d{4})$")

    # Заменяем NaN в кэшбэке на 0
    df["Кэшбэк"] = df["Кэшбэк"].fillna(0)

    return df
