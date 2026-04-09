import pytest
from src.database.postgres_client import PostgresClient


def test_db_connection():
    """Проверка подключения к БД"""
    db = PostgresClient()
    tables = db.get_table_names()
    assert isinstance(tables, list)
    assert len(tables) > 0, "База данных пуста, таблицы не найдены!"


def test_get_schema():
    """Проверка получения схемы таблицы"""
    db = PostgresClient()
    tables = db.get_table_names()
    schema = db.get_schema_info_for_table(tables[0])
    assert isinstance(schema, str)
    assert len(schema) > 0
