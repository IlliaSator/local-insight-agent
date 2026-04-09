<div align="center">

# InsightData Analyst

**RAG-Enhanced SQL Agent · Powered by Local LLM**

Ask questions about your database in plain language — no cloud, no data leaks

---

## About

**InsightData Analyst** is an intelligent data analysis agent that translates natural language questions into precise SQL queries. The system runs **entirely locally** — no external APIs, no data sent to the cloud.

The agent does not guess the database structure. It retrieves actual table schemas from a vector store (RAG) and generates SQL based on the real data architecture. If a query fails, the agent analyses the traceback and corrects the code automatically.

| | |
|---|---|
| ![UI](./assets/image.png) | ![Logs](./assets/image1.png) |
| Chat interface | Agent execution logs |

---

## How It Works

**1. Retrieval** — The user's question is used to search Qdrant for the most relevant table schemas (by vector similarity).

**2. Generation** — The model receives the schema context and generates a SQL query via LangGraph.

**3. Execution** — The SQL tool runs the query against PostgreSQL 15.

**4. Self-Correction** — If the query fails, the agent receives the traceback and retries automatically (up to 25 attempts). On success, the result is returned to the user.

---

## Features

| Feature | Description |
|---|---|
| Natural Language to SQL | Ask questions in plain language, get precise queries |
| RAG Metadata Retrieval | Real table schemas from Qdrant — no hallucinations |
| Self-Correction Loop | Automatic SQL error fixing, up to 25 iterations |
| 100% Local | Ollama + local DB — data never leaves your machine |
| Docker-First | One command brings up the entire infrastructure |
| Pytest Coverage | Automated tests for critical agent nodes and SQL tools |

---

## Tech Stack

| Layer | Technology |
|---|---|
| LLM | Ollama · `qwen2.5-coder:3b` |
| Agent | LangGraph · LangChain |
| Database | PostgreSQL 15 |
| Vector Store | Qdrant |
| Frontend | Streamlit |
| Testing | pytest |
| Deploy | Docker · Docker Compose |

---

## Project Structure

- 📁 **insight-data-analyst/**
  - 📁 assets/
  - 📁 data/
    - 📁 processed/
    - 📁 raw/
  - 📁 docker/
    - 📁 postgres/
    - 📁 qdrant/
  - 📁 notebooks/
  - 📁 scripts/
    - 🐍 db_filler.py
    - 🐍 index_db.py
  - 📁 src/
    - 📁 api/
      - 🐍 app.py
    - 📁 core/
      - 🐍 config.py
      - 🐍 logger.py
    - 📁 database/
      - 🐍 postgres_client.py
      - 🐍 vector_store.py
    - 📁 services/
      - 📁 agent/
        - 🐍 graph.py
        - 🐍 state.py
      - 📁 llm/
        - 🐍 ollama_client.py
        - 🐍 prompts.py
    - 📁 tools/
      - 🐍 sql_executor.py
  - 📁 tests/
    - 🐍 test_agent.py
    - 🐍 test_db.py
  - 🐍 main.py
  - 🐳 Dockerfile
  - 🐳 docker-compose.yml
  - ⚙️ entrypoint.sh
  - 📄 requirements.txt
  - 📄 .env.example

**Prerequisites:** [Docker](https://docs.docker.com/get-docker/) & [Ollama](https://ollama.com/)

**1. Pull the model**
```bash
ollama pull qwen2.5-coder:3b
```

**2. Clone and configure**
```bash
git clone https://github.com/IlliaSator/insight-data-analyst.git
cd insight-data-analyst
cp .env.example .env
```

**3. Run**
```bash
docker-compose up --build
```

The system automatically starts PostgreSQL, populates it with CSV data, and indexes table schemas in Qdrant.

**4. Open** `http://localhost:8501`

---

## Testing

Tests run inside the container since the agent depends on PostgreSQL, Qdrant, and Ollama.

```bash
# Run all tests
docker exec -it insight_app python -m pytest

# Verbose output
docker exec -it insight_app python -m pytest -s tests/test_agent.py
```

---
---

<div align="center">

# InsightData Analyst

**RAG-агент для SQL · На базе локальной LLM**

Задавайте вопросы к базе данных на естественном языке — без облака, без утечек данных

</div>

---

## О проекте

**InsightData Analyst** — интеллектуальный агент для анализа данных, который переводит вопросы на естественном языке в точные SQL-запросы. Система работает **полностью локально**: нет внешних API, нет передачи данных в облако.

Агент не угадывает структуру базы данных. Он извлекает актуальные схемы таблиц из векторного хранилища (RAG) и генерирует SQL с учётом реальной архитектуры данных. При ошибке агент анализирует трейсбек и самостоятельно исправляет запрос.

---

## Как это работает

**1. Retrieval** — Вопрос пользователя используется для поиска релевантных схем таблиц в Qdrant (по векторному сходству).

**2. Generation** — Модель получает контекст схем и генерирует SQL-запрос через LangGraph.

**3. Execution** — SQL-инструмент выполняет запрос в PostgreSQL 15.

**4. Self-Correction** — При ошибке агент получает трейсбек и повторяет попытку автоматически (до 25 раз). При успехе результат возвращается пользователю.

---

## Возможности

| Возможность | Описание |
|---|---|
| Natural Language to SQL | Задавайте вопросы обычным языком, получайте точные запросы |
| RAG Metadata Retrieval | Актуальные схемы таблиц из Qdrant, а не галлюцинации модели |
| Self-Correction Loop | Автоматическое исправление ошибок SQL, до 25 итераций |
| 100% локально | Ollama + локальная БД — данные не покидают машину |
| Docker-First | Одна команда поднимает всю инфраструктуру |
| Pytest Coverage | Автотесты критических узлов агента и SQL-инструментов |

---

## Технологический стек

| Слой | Технология |
|---|---|
| LLM | Ollama · `qwen2.5-coder:3b` |
| Agent | LangGraph · LangChain |
| Database | PostgreSQL 15 |
| Vector Store | Qdrant |
| Frontend | Streamlit |
| Testing | pytest |
| Deploy | Docker · Docker Compose |

---

## Структура проекта

- 📁 **insight-data-analyst/**
  - 📁 assets/
  - 📁 data/
    - 📁 processed/
    - 📁 raw/
  - 📁 docker/
    - 📁 postgres/
    - 📁 qdrant/
  - 📁 notebooks/
  - 📁 scripts/
    - 🐍 db_filler.py
    - 🐍 index_db.py
  - 📁 src/
    - 📁 api/
      - 🐍 app.py
    - 📁 core/
      - 🐍 config.py
      - 🐍 logger.py
    - 📁 database/
      - 🐍 postgres_client.py
      - 🐍 vector_store.py
    - 📁 services/
      - 📁 agent/
        - 🐍 graph.py
        - 🐍 state.py
      - 📁 llm/
        - 🐍 ollama_client.py
        - 🐍 prompts.py
    - 📁 tools/
      - 🐍 sql_executor.py
  - 📁 tests/
    - 🐍 test_agent.py
    - 🐍 test_db.py
  - 🐍 main.py
  - 🐳 Dockerfile
  - 🐳 docker-compose.yml
  - ⚙️ entrypoint.sh
  - 📄 requirements.txt
  - 📄 .env.example

**Требования:** [Docker](https://docs.docker.com/get-docker/) & [Ollama](https://ollama.com/)

**1. Скачать модель**
```bash
ollama pull qwen2.5-coder:3b
```

**2. Клонировать и настроить**
```bash
git clone https://github.com/IlliaSator/insight-data-analyst.git
cd insight-data-analyst
cp .env.example .env
```

**3. Запустить**
```bash
docker-compose up --build
```

Система автоматически поднимет PostgreSQL, наполнит базу данными из CSV и проиндексирует метаданные схем в Qdrant.

**4. Открыть** `http://localhost:8501`

---

## Тестирование

Тесты запускаются внутри контейнера, так как агент зависит от PostgreSQL, Qdrant и Ollama.

```bash
# Запуск всех тестов
docker exec -it insight_app python -m pytest

# Подробный вывод
docker exec -it insight_app python -m pytest -s tests/test_agent.py
```