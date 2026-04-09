import pytest
from src.services.agent.graph import graph


def test_agent_workflow():
    """Интеграционный тест: проходит ли вопрос через весь граф"""

    test_input = {"question": "Покажи 3 любых товара",
                  "error_history": [], "retry_count": 0}

    config = {"recursion_limit": 15}

    result = graph.invoke(test_input, config)

    assert "final_answer" in result
    assert len(result["final_answer"]) > 0

    print(f"\nАгент ответил: {result['final_answer']}")


if __name__ == "__main__":

    test_agent_workflow()
