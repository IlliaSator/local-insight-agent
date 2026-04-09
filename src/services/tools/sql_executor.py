import psycopg2
from src.core.config import Config
from src.core.logger import logger


class SQLExecutor:
    def __init__(self):
        self.conn_str = Config.DB_URL

    def execute(self, query: str):
        """Метод должен называться именно execute, как в graph.py"""
        try:
            # Убираем лишние точки с запятой, если они есть
            query = query.strip().rstrip(';')

            with psycopg2.connect(self.conn_str) as conn:
                with conn.cursor() as cur:
                    cur.execute(query)
                    # Если запрос что-то возвращает (SELECT)
                    if cur.description:
                        columns = [desc[0] for desc in cur.description]
                        results = cur.fetchall()
                        # Возвращаем список словарей для удобства LLM
                        return [dict(zip(columns, row)) for row in results], None

                    conn.commit()
                    return "Success", None
        except Exception as e:
            logger.error(f"Ошибка выполнения SQL: {e}")
            return None, str(e)
