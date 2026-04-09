from typing import TypedDict, Annotated, List
import operator


class AgentState(TypedDict):
    # Текущий вопрос пользователя
    question: str
    # Сгенерированный SQL запрос
    sql_query: str
    # Результат из базы
    db_result: str
    # История ошибок для самокоррекции (Annotated + operator.add позволяет накапливать список)
    error_history: Annotated[List[str], operator.add]
    # Финальный ответ
    final_answer: str
