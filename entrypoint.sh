#!/bin/bash
set -e

echo "--- ⏳ Ожидание базы данных (db:5432)... ---"
until pg_isready -h db -p 5432 -U admin; do
  echo "База данных недоступна, ждем..."
  sleep 2
done

echo "--- 📦 Наполнение базы (db_filler)... ---"
python -m scripts.db_filler

echo "--- 🔍 Индексация схем (index_db)... ---"
python -m scripts.index_db

echo "--- 🚀 Запуск Streamlit... ---"
exec python -m streamlit run src/api/app.py --server.port=8501 --server.address=0.0.0.0