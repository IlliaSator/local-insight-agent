import re
from langgraph.graph import StateGraph, END, START
from src.services.agent.state import AgentState
from src.services.llm.ollama_client import OllamaManager
from src.services.tools.sql_executor import SQLExecutor
from src.database.vector_store import VectorStore
from src.services.llm.prompts import SQL_GENERATION_PROMPT
from src.core.logger import logger


def generate_sql_node(state: AgentState):
    # Увеличиваем счетчик попыток
    current_retry = state.get('retry_count', 0)
    logger.info(f"--- ШАГ: ГЕНЕРАЦИЯ SQL (Попытка {current_retry + 1}) ---")

    llm = OllamaManager()
    vs = VectorStore()

    relevant_schemas = vs.search_relevant_tables(state['question'], limit=5)
    schema_context = "\n".join(relevant_schemas)

    prompt = SQL_GENERATION_PROMPT.format(
        schema_context=schema_context,
        user_question=state['question']
    )

    if state.get('error_history'):
        prompt += f"\n\n### ВАЖНО: Твой предыдущий запрос выдал ошибку. НЕ ПОВТОРЯЙ ЕЁ:\n{state['error_history'][-1]}"

    response = llm.chat(prompt).strip()
    sql_clean = re.sub(r'```sql|```', '', response,
                       flags=re.IGNORECASE).strip()

    return {"sql_query": sql_clean, "retry_count": current_retry + 1}


def execute_sql_node(state: AgentState):
    logger.info("--- ШАГ: ВЫПОЛНЕНИЕ SQL ---")
    executor = SQLExecutor()
    result, error = executor.execute(state['sql_query'])

    if error:
        # Если ошибка, записываем её и НЕ очищаем db_result
        return {
            "error_history": state.get('error_history', []) + [str(error)],
            "db_result": None
        }

    # Если успех — ОБЯЗАТЕЛЬНО очищаем error_history и записываем результат
    return {
        "db_result": str(result),
        "error_history": []
    }


def should_continue(state: AgentState):
    # 1. Если в стейте есть данные и НЕТ свежих ошибок — идем к финалу
    if state.get('db_result') and not state.get('error_history'):
        logger.info("🎯 Успех! Переходим к ответу.")
        return "finalize"

    # 2. Если есть ошибки и мы не превысили лимит (например, 3 попытки)
    if state.get('error_history') and state.get('retry_count', 0) < 3:
        logger.warning("🔄 Ошибка БД, пробуем перегенерировать SQL...")
        return "generate"

    # 3. В остальных случаях (лимит исчерпан или данных нет) — финализируем
    return "finalize"


def finalize_node(state: AgentState):
    logger.info("--- ШАГ: ФИНАЛИЗАЦИЯ ---")
    llm = OllamaManager()

    if not state.get('db_result'):
        answer = "К сожалению, я не смог получить данные из базы после нескольких попыток."
    else:
        prompt = f"Вопрос пользователя: {state['question']}\nДанные из БД: {state['db_result']}\nСформулируй краткий ответ."
        answer = llm.chat(prompt)

    return {"final_answer": answer}


# Сборка графа
workflow = StateGraph(AgentState)

workflow.add_node("generate", generate_sql_node)
workflow.add_node("execute", execute_sql_node)
workflow.add_node("finalize", finalize_node)

workflow.add_edge(START, "generate")
workflow.add_edge("generate", "execute")

workflow.add_conditional_edges(
    "execute",
    should_continue,
    {
        "generate": "generate",
        "finalize": "finalize"
    }
)

workflow.add_edge("finalize", END)

graph = workflow.compile()
