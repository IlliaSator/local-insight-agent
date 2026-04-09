import os
import pandas as pd
from sqlalchemy import create_engine
from src.core.config import Config

# Создаем подключение к базе
engine = create_engine(Config.DB_URL)


def upload_extra_tables():
    # Определяем базовый путь к проекту
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # Указываем путь к папке с сырыми данными
    raw_data_path = os.path.join(base_path, "data", "raw")

    # Словарь таблиц
    # Словарь всех необходимых таблиц
    extra_tables = {
        "order_items": "olist_order_items_dataset.csv",
        "order_payments": "olist_order_payments_dataset.csv",
        "products": "olist_products_dataset.csv",
        "orders": "olist_orders_dataset.csv",
        "customers": "olist_customers_dataset.csv"
    }

    for table_name, file_name in extra_tables.items():
        # Собираем полный путь: корень/data/raw/имя_файла.csv
        file_path = os.path.join(raw_data_path, file_name)

        if not os.path.exists(file_path):
            print(f"❌ ОШИБКА: Файл не найден: {file_path}")
            continue

        print(f"Загрузка {table_name} из {file_name}...")
        try:
            df = pd.read_csv(file_path)
            # Загружаем в Postgres
            df.to_sql(table_name, engine, if_exists='replace', index=False)
            print(f"✅ Таблица {table_name} успешно загружена.")
        except Exception as e:
            print(f"❌ Произошла ошибка при загрузке {table_name}: {e}")


if __name__ == "__main__":
    upload_extra_tables()
