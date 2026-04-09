import ollama
# Импортируем наш созданный класс Config
from src.core.config import Config


class OllamaManager:
    def __init__(self, model_name=None):
        # Если при создании объекта модель не указана, берем ту, что в конфиге (gemma2:2b)
        self.model_name = model_name or Config.OLLAMA_MODEL
        # Используем URL из конфига
        self.client = ollama.Client(host=Config.OLLAMA_URL)

    def chat(self, prompt):
        try:
            response = self.client.generate(
                model=self.model_name, prompt=prompt)
            return response['response']
        except Exception as e:
            return f"Ошибка при обращении к Ollama: {str(e)}"
