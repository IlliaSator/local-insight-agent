import logging
import sys
import os
from datetime import datetime

# Создаем папку для логов, если её нет
LOGS_DIR = os.path.join(os.path.dirname(
    os.path.dirname(os.path.dirname(__file__))), "logs")
if not os.path.exists(LOGS_DIR):
    os.makedirs(LOGS_DIR)


def setup_logger(name: str):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # Формат сообщений
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # 1. Обработчик для записи в файл
    log_file = os.path.join(
        LOGS_DIR, f"{datetime.now().strftime('%Y-%m-%d')}.log")
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setFormatter(formatter)

    # 2. Обработчик для вывода в консоль
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)

    # Добавляем обработчики, если они еще не добавлены
    if not logger.handlers:
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger


# Создаем основной логгер проекта
logger = setup_logger("insight_agent")
