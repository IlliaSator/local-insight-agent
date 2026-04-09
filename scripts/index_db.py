from src.core.logger import logger
from src.database.vector_store import VectorStore
from src.database.postgres_client import PostgresClient
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def main():
    try:
        db = PostgresClient()
        vs = VectorStore()
        # КРИТИЧНО: имя должно совпадать с VectorStore в graph.py
        collection_name = "schemas"

        # Очищаем старое, чтобы не было дублей
        try:
            if vs.client.collection_exists(collection_name):
                logger.info(f"Очистка старой коллекции {collection_name}...")
                vs.client.delete_collection(collection_name)

            from qdrant_client.http import models
            vs.client.create_collection(
                collection_name=collection_name,
                vectors_config=models.VectorParams(
                    size=384, distance=models.Distance.COSINE)
            )
            logger.info(f"Создана чистая коллекция {collection_name}")
        except Exception as coll_err:
            logger.warning(f"Ошибка при подготовке коллекции: {coll_err}")

        logger.info("Запуск индексации схем...")
        tables = db.get_table_names()

        for table in tables:
            try:
                columns = db.get_schema_info_for_table(table)
                metadata_text = f"Таблица: {table}. Колонки: {columns}"
                # Передаем table_name как ID, чтобы избежать дубликатов внутри коллекции
                vs.add_metadata(table, metadata_text)
                logger.info(f"✅ Индексирована таблица: {table}")
            except Exception as e:
                logger.error(f"Ошибка при индексации {table}: {e}")

        logger.info("Индексация завершена успешно.")

    except Exception as e:
        logger.error(f"Глобальная ошибка скрипта: {e}")


if __name__ == "__main__":
    main()
