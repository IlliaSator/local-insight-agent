import sys
import os
from src.core.logger import logger

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from src.services.agent.graph import app
    logger.info("LangGraph App успешно скомпилирован.")
except Exception as e:
    logger.critical(f"Ошибка импорта графа: {e}")
    sys.exit(1)


def run_chat():
    print("\n🕵️ INSIGHT-LOCAL: АНАЛИТИК ГОТОВ")

    while True:
        user_input = input("\n❓ Вопрос: ")
        if user_input.lower() in ['exit', 'quit', 'выход']:
            break

        inputs = {"question": user_input, "error_history": []}
        try:
            logger.info(f"Пользователь задал вопрос: {user_input}")
            result = app.invoke(inputs, {"recursion_limit": 20})
            print(f"\n🤖 Ответ: {result['final_answer']}")
        except Exception as e:
            logger.error(f"Ошибка при обработке вопроса: {e}")
            print("❌ Произошла ошибка. Подробности в логах.")


if __name__ == "__main__":
    run_chat()
