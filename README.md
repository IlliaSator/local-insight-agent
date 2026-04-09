    InsightData Analyst: RAG-Enhanced SQL Agent
InsightData Analyst — это интеллектуальный ассистент для анализа данных, который переводит естественный язык в SQL-запросы. Система использует архитектуру RAG (Retrieval-Augmented Generation) для извлечения схем баз данных из векторного хранилища и агентный подход на базе LangGraph для генерации, выполнения и самоисправления SQL-кода.

![Streamlit UI](./assets/image.png)

![Agent Logs](./assets/image1.png)

    Основные возможности
Natural Language to SQL: Задавайте вопросы к базе данных на обычном языке.

RAG Metadata Retrieval: Агент не «гадает» структуру БД, а получает актуальные схемы из Qdrant.

Self-Correction Loop: Если SQL-запрос вызывает ошибку в Postgres, агент анализирует трейсбек и исправляет код (до 25 попыток).

Docker-First: Полная изоляция приложения, БД и векторного хранилища.

🏗 Структура проекта
Проект организован по принципам модульности:
├── data/raw/            # Исходные CSV датасеты (Olist)
├── scripts/             # Скрипты наполнения БД и индексации схем
├── src/
│   ├── api/             # Интерфейс на Streamlit
│   ├── core/            # Конфигурация и логгер
│   ├── database/        # Клиенты Postgres и Qdrant
│   ├── services/
│   │   ├── agent/       # Логика LangGraph (графы, состояния)
│   │   └── llm/         # Интеграция с Ollama
│   └── tools/           # Инструменты выполнения SQL
├── Dockerfile           # Инструкции сборки приложения
├── docker-compose.yml   # Оркестрация всей системы
└── entrypoint.sh        # Скрипт автоматического запуска "из коробки"

🛠 Технологический стек
LLM: Ollama (модель qwen2.5-coder:3b — оптимизирована под генерацию кода).

Agentic Framework: LangGraph / LangChain.

Database: PostgreSQL 15.

Vector Store: Qdrant (хранение эмбеддингов схем таблиц).

Frontend: Streamlit.

## Тестирование

Проект использует `pytest` для автоматизированной проверки критических узлов агента и корректности выполнения SQL-запросов.

### Запуск тестов в Docker (рекомендуется)
Так как агент зависит от инфраструктуры (PostgreSQL, Qdrant, Ollama), тесты запускаются внутри контейнера приложения:

```bash
# Запуск всех тестов
docker exec -it insight_app python -m pytest

# Запуск с подробным логом шагов агента
docker exec -it insight_app python -m pytest -s tests/test_agent.py

 Быстрый запуск
1. Подготовка
Убедитесь, что у вас установлены Docker и Ollama.
В терминале скачайте модель:
ollama pull qwen2.5-coder:3b
2. Настройка окружения
Склонируйте репозиторий и создайте .env:
cp .env.example .env
3. Запуск одной командой
Система автоматически поднимет базу, наполнит её данными из CSV и проиндексирует метаданные:
docker-compose up --build
После запуска интерфейс будет доступен по адресу: http://localhost:8501

🔍 Как это работает?
Retrieval: При получении вопроса система ищет наиболее релевантные описания таблиц в Qdrant.

Generation: Модель получает контекст (схемы таблиц) и генерирует SQL.

Execution: SQL-инструмент выполняет запрос в Postgres.

Verification: В случае ошибки (например, column does not exist), агент получает текст ошибки и делает повторную попытку.