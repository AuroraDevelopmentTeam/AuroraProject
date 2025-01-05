import os
import logging
from logging.handlers import RotatingFileHandler
import nextcord
from nextcord.ext import commands
from dotenv import load_dotenv
from config import settings

import warnings
warnings.filterwarnings('ignore')
load_dotenv()
token = os.getenv("token")

# Настройка форматтера для логов
log_formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s - [%(filename)s:%(lineno)d] - %(funcName)s"
)

# Настройка обработчиков логирования
general_handler = RotatingFileHandler(
    "general.log", maxBytes=1 * 1024 * 1024, backupCount=1, encoding="utf-8"
)
general_handler.setLevel(logging.INFO)
general_handler.setFormatter(log_formatter)

debug_handler = RotatingFileHandler(
    "debug.log", maxBytes=1 * 1024 * 1024, backupCount=1, encoding="utf-8"
)
debug_handler.setLevel(logging.DEBUG)
debug_handler.setFormatter(log_formatter)

error_handler = RotatingFileHandler(
    "error.log", maxBytes=1 * 1024 * 1024, backupCount=1, encoding="utf-8"
)
error_handler.setLevel(logging.ERROR)
error_handler.setFormatter(log_formatter)

# Основная настройка логирования
logging.basicConfig(level=logging.DEBUG, handlers=[general_handler, debug_handler, error_handler])

# Консольный обработчик для вывода WARNINGS и ошибок в консоль
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.WARNING)
console_handler.setFormatter(log_formatter)

logging.getLogger().addHandler(console_handler)

# Инициализация бота
intents = nextcord.Intents.all()
client = commands.AutoShardedBot(
    command_prefix=settings["PREFIX"],
    case_insensitive=True,
    intents=intents,
    activity=nextcord.Game(name="You cute! /help"),
    shard_count=1,
)

# Функция для загрузки cogs и их логирования
if __name__ == "__main__":
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            try:
                client.load_extension(f"cogs.{filename[: -3]}")
                logging.info(f"Загружен cog: {filename[: -3]}")
            except Exception as e:
                logging.error(f"Ошибка при загрузке {filename}: {e}", exc_info=True)
    logging.info("Запуск бота...")
    client.run(token, reconnect=True)
