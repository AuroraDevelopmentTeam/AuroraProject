import logging
from pathlib import Path
import importlib
import pkgutil
from typing import List, Optional

from aurorabot.bot import AuroraBot


class ExtensionLoader:
    def __init__(self, bot: AuroraBot, logger: logging.Logger):
        self.bot = bot
        self.logger = logger
        self.base_path = Path(__file__).parent.parent

    async def load_extensions(self) -> None:
        """Загрузка всех расширений (когов) из директории commands."""
        commands_path = self.base_path / "commands"
        if not commands_path.exists():
            self.logger.warning("Директория commands не найдена")
            return

        # Загрузка всех модулей в директории commands
        for _, name, is_pkg in pkgutil.iter_modules([str(commands_path)]):
            if is_pkg:
                try:
                    # Загрузка пакета
                    package = importlib.import_module(f"aurorabot.commands.{name}")
                    # Поиск и загрузка всех модулей в пакете
                    for _, module_name, _ in pkgutil.iter_modules([str(commands_path / name)]):
                        try:
                            await self.bot.load_extension(f"aurorabot.commands.{name}.{module_name}")
                            self.logger.info(f"Загружено расширение: aurorabot.commands.{name}.{module_name}")
                        except Exception as e:
                            self.logger.error(f"Ошибка при загрузке расширения {module_name}: {e}")
                except Exception as e:
                    self.logger.error(f"Ошибка при загрузке пакета {name}: {e}")

    async def load_events(self) -> None:
        """Загрузка всех обработчиков событий из директории events."""
        events_path = self.base_path / "events"
        if not events_path.exists():
            self.logger.warning("Директория events не найдена")
            return

        # Загрузка всех модулей в директории events
        for _, name, is_pkg in pkgutil.iter_modules([str(events_path)]):
            if is_pkg:
                try:
                    # Загрузка пакета
                    package = importlib.import_module(f"aurorabot.events.{name}")
                    # Поиск и загрузка всех модулей в пакете
                    for _, module_name, _ in pkgutil.iter_modules([str(events_path / name)]):
                        try:
                            await self.bot.load_extension(f"aurorabot.events.{name}.{module_name}")
                            self.logger.info(f"Загружен обработчик событий: aurorabot.events.{name}.{module_name}")
                        except Exception as e:
                            self.logger.error(f"Ошибка при загрузке обработчика событий {module_name}: {e}")
                except Exception as e:
                    self.logger.error(f"Ошибка при загрузке пакета событий {name}: {e}") 