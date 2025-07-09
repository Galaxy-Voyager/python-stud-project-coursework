import pandas as pd

# Загрузка файла
df = pd.read_excel("data/operations.xlsx")

# Вывод названий столбцов
print("Список столбцов в файле:")
print(df.columns.tolist())

# Вывод первых строк для проверки
print("\nПервые 3 строки данных:")
print(df.head(3))
