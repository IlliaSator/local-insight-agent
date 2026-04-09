import os
from qdrant_client import QdrantClient
from qdrant_client.http import models
from sentence_transformers import SentenceTransformer
from src.core.logger import logger


class VectorStore:
    def __init__(self):
        # Читаем настройки из .env (внутри Docker это 'qdrant')
        host = os.getenv("QDRANT_HOST", "qdrant")
        port = os.getenv("QDRANT_PORT", "6333")

        try:
            self.client = QdrantClient(host=host, port=int(port))
            # КРИТИЧНО: Имя должно быть таким же, как в index_db.py
            self.collection_name = "schemas"

            # Модель эмбеддингов
            self.encoder = SentenceTransformer('all-MiniLM-L6-v2')
            logger.info(
                f"VectorStore успешно подключен к {host}:{port}, коллекция: {self.collection_name}")
        except Exception as e:
            logger.error(f"Ошибка инициализации QdrantClient: {e}")
            raise

    def search_relevant_tables(self, query: str, limit=3):
        try:
            query_vector = self.encoder.encode(query).tolist()
            # Поиск через query_points
            response = self.client.query_points(
                collection_name=self.collection_name,
                query=query_vector,
                limit=limit
            )
            return [res.payload['schema'] for res in response.points if res.payload]
        except Exception as e:
            logger.error(f"Ошибка поиска в Qdrant: {e}")
            # Резервный метод поиска
            try:
                res = self.client.search(
                    collection_name=self.collection_name,
                    query_vector=query_vector,
                    limit=limit
                )
                return [r.payload['schema'] for r in res]
            except:
                return []

    def add_metadata(self, table_name: str, schema_text: str):
        """Добавление информации о таблице в векторную базу"""
        try:
            self.client.upsert(
                collection_name=self.collection_name,
                points=[
                    models.PointStruct(
                        # Используем хэш от имени таблицы для стабильного ID
                        id=abs(hash(table_name)) % 10**8,
                        vector=self.encoder.encode(schema_text).tolist(),
                        payload={
                            "table_name": table_name,
                            "schema": schema_text
                        }
                    )
                ]
            )
            logger.info(
                f"Метаданные таблицы {table_name} успешно добавлены в {self.collection_name}.")
        except Exception as e:
            logger.error(f"Ошибка при добавлении метаданных {table_name}: {e}")
