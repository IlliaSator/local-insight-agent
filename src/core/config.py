import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    # --- LLM ---
    # В Docker переменная OLLAMA_URL перекроет дефолт
    OLLAMA_BASE_URL = os.getenv("OLLAMA_URL", os.getenv(
        "OLLAMA_BASE_URL", "http://localhost:11434"))
    OLLAMA_URL = OLLAMA_BASE_URL
    MODEL_NAME = os.getenv("MODEL_NAME", "qwen2.5-coder:3b")
    OLLAMA_MODEL = MODEL_NAME  # Исправляет ошибку из image_5dc9c9.png

    # --- DATABASE ---
    DB_USER = os.getenv("POSTGRES_USER", "admin")
    DB_PASS = os.getenv("POSTGRES_PASSWORD", "secret")
    DB_HOST = os.getenv("POSTGRES_HOST", "localhost")  # Docker подставит 'db'
    DB_PORT = os.getenv("POSTGRES_PORT", "5432")
    DB_NAME = os.getenv("POSTGRES_DB", "insight_db")

    DATABASE_URL = os.getenv(
        "DATABASE_URL", f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}")
    DB_URL = DATABASE_URL

    # --- VECTOR ---
    QDRANT_HOST = os.getenv("QDRANT_HOST", "localhost")
    QDRANT_PORT = int(os.getenv("QDRANT_PORT", 6333))
