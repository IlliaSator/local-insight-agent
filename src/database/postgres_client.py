from sqlalchemy import create_engine, inspect
from src.core.config import Config
from src.core.logger import logger


class PostgresClient:
    def __init__(self):
        self.engine = create_engine(Config.DB_URL)
        self._inspector = None

    def get_table_names(self):
        if self._inspector is None:
            self._inspector = inspect(self.engine)
        return self._inspector.get_table_names()

    def get_schema_info_for_table(self, table_name):
        if self._inspector is None:
            self._inspector = inspect(self.engine)
        columns = [col['name']
                   for col in self._inspector.get_columns(table_name)]
        return ", ".join(columns)

    def get_schema_info(self):
        if self._inspector is None:
            self._inspector = inspect(self.engine)

        schema_info = ""
        for table_name in self.get_table_names():
            schema_info += f"\nТаблица: {table_name}\nКолонки: "
            columns = [col['name']
                       for col in self._inspector.get_columns(table_name)]
            schema_info += ", ".join(columns) + "\n"

        return schema_info


if __name__ == "__main__":
    db = PostgresClient()
    try:
        tables = db.get_table_names()
        logger.info(f"Успешное подключение! Найденные таблицы: {tables}")
    except Exception as e:
        logger.error(f"Ошибка подключения: {e}")
