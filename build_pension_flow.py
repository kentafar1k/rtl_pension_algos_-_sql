import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

# Настройки
INPUT_FILE = 'Данные.xlsx'
OUTPUT_FILE = 'Данные.xlsx'  # Можно сохранить в новый файл, если нужно
SHEET_DOGOVORS = 0  # Первый лист: договоры
SHEET_PENSIONS = 1   # Второй лист: пенсии
SHEET_PARAMS = 2     # Третий лист: параметры
SHEET_RESULT = 'Результат'

# Чтение данных
df_dog = pd.read_excel(INPUT_FILE, sheet_name=SHEET_DOGOVORS)
df_pens = pd.read_excel(INPUT_FILE, sheet_name=SHEET_PENSIONS)
df_params = pd.read_excel(INPUT_FILE, sheet_name=SHEET_PARAMS, header=None)

# Парсинг параметров
report_date = pd.to_datetime(df_params.iloc[0, 1], dayfirst=True)
index_rate = float(str(df_params.iloc[1, 1]).replace('%','')) / 100
max_age = int(df_params.iloc[2, 1])

# Подготовка
df = df_dog.merge(df_pens, on='Номер договора')

results = []

for idx, row in df.iterrows():
    contract = row['Номер договора']
    dob = pd.to_datetime(row['Дата рождения участника'], dayfirst=True)
    pens_age = int(row['Пенсионный возраст'])
    stage = 'накопления'  # Можно добавить столбец "Этап" при необходимости
    base_pension = row['Установленный размер пенсии']

    # Определяем дату выхода на пенсию
    pension_start = dob + relativedelta(years=pens_age)
    if pension_start < report_date:
        pension_start = report_date  # Если уже на пенсии

    # Дата последнего платежа
    end_date = dob + relativedelta(years=max_age)

    # Генерируем даты платежей
    pay_dates = []
    pay_date = pension_start.replace(day=1) + relativedelta(months=1) - timedelta(days=1)  # последний день месяца
    while pay_date <= end_date:
        pay_dates.append(pay_date)
        pay_date = (pay_date + relativedelta(months=1)).replace(day=1) + relativedelta(months=1) - timedelta(days=1)

    # Генерируем суммы пенсий
    pensions = []
    current_pension = base_pension
    for i, dt in enumerate(pay_dates):
        # Индексация в январе
        if i > 0 and dt.month == 1:
            current_pension *= (1 + index_rate)
        pensions.append(round(current_pension, 2))

    # Заполняем результат
    for dt, val in zip(pay_dates, pensions):
        results.append({
            'Номер договора': contract,
            'Дата платежа': dt.strftime('%d.%m.%Y'),
            'Размер пенсии': val
        })

# Сохраняем результат
df_result = pd.DataFrame(results)
with pd.ExcelWriter(OUTPUT_FILE, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
    df_result.to_excel(writer, sheet_name=SHEET_RESULT, index=False)

# Примечание по большим данным
'''
Для обработки больших данных, когда всё не помещается в память:
- Используйте пакетную обработку (chunking) с помощью pandas.read_excel(..., chunksize=...).
- Для хранения результатов используйте базы данных (например, PostgreSQL, ClickHouse) или форматы, поддерживающие стриминг (Parquet, CSV с построчной записью).
- Для расчётов используйте генераторы или Dask, Spark, если требуется распределённая обработка.
- Не загружайте все данные в DataFrame одновременно, а обрабатывайте по частям, выгружая результат сразу на диск или в БД.
''' 