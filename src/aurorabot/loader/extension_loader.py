import os
import logging
import asyncio
from pathlib import Path
import importlib
import pkgutil
from typing import List, Optional, TYPE_CHECKING
from nextcord.ext import commands
from aurorabot.core.services.logger_service import LoggerService

if TYPE_CHECKING:
    from aurorabot.bot import AuroraBot


class ExtensionLoader:
    """Loader for bot extensions."""
    
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.logger = bot.logger
        self.loaded_extensions: List[str] = []
        self.base_path = Path(__file__).parent.parent

    async def load_extensions(self) -> None:
        """Load all extensions from the commands directory."""
        self.logger.info("Starting to load command extensions...")
        commands_path = self.base_path / "commands"
        
        if not commands_path.exists():
            self.logger.warning(f"Commands directory not found at {commands_path}")
            return
            
        # Load all modules in the commands directory
        for _, name, is_pkg in pkgutil.iter_modules([str(commands_path)]):
            if is_pkg:
                # Load package
                package_path = commands_path / name
                self.logger.info(f"Loading package: {name}")
                
                # Load all modules in the package
                for _, module_name, _ in pkgutil.iter_modules([str(package_path)]):
                    try:
                        module = importlib.import_module(f"aurorabot.commands.{name}.{module_name}")
                        if hasattr(module, 'setup'):
                            try:
                                cog = await module.setup(self.bot)
                                if cog is not None:
                                    self.bot.add_cog(cog)
                                    self.loaded_extensions.append(f"{name}.{module_name}")
                                    self.logger.info(f"Loaded extension: {name}.{module_name}")
                                else:
                                    self.logger.error(f"Setup function returned None for {name}.{module_name}")
                            except Exception as e:
                                self.logger.error(f"Error in setup function for {name}.{module_name}: {e}", exc_info=True)
                    except Exception as e:
                        self.logger.error(f"Failed to load extension {module_name}: {e}", exc_info=True)
            else:
                # Load single module
                try:
                    module = importlib.import_module(f"aurorabot.commands.{name}")
                    if hasattr(module, 'setup'):
                        try:
                            cog = await module.setup(self.bot)
                            if cog is not None:
                                self.bot.add_cog(cog)
                                self.loaded_extensions.append(name)
                                self.logger.info(f"Loaded extension: {name}")
                            else:
                                self.logger.error(f"Setup function returned None for {name}")
                        except Exception as e:
                            self.logger.error(f"Error in setup function for {name}: {e}", exc_info=True)
                except Exception as e:
                    self.logger.error(f"Failed to load module {name}: {e}", exc_info=True)
                    
        # Sync application commands
        try:
            self.logger.info("Syncing application commands...")
            synced = await self.bot.sync_application_commands()
            if synced is not None:
                self.logger.info(f"Synced {len(synced)} commands")
            else:
                self.logger.warning("Command sync returned None")
        except Exception as e:
            self.logger.error(f"Failed to sync commands: {e}", exc_info=True)
            
        # Log loaded commands
        commands = self.bot.get_application_commands()
        self.logger.info(f"Loaded {len(commands)} commands: {[cmd.name for cmd in commands]}")
        
    async def load_events(self) -> None:
        """Load all extensions from the events directory."""
        self.logger.info("Starting to load event extensions...")
        events_path = self.base_path / "events"
        
        if not events_path.exists():
            self.logger.warning(f"Events directory not found at {events_path}")
            return
            
        # Load all modules in the events directory
        for _, name, is_pkg in pkgutil.iter_modules([str(events_path)]):
            if is_pkg:
                # Load package
                package_path = events_path / name
                self.logger.info(f"Loading package: {name}")
                
                # Load all modules in the package
                for _, module_name, _ in pkgutil.iter_modules([str(package_path)]):
                    try:
                        module = importlib.import_module(f"aurorabot.events.{name}.{module_name}")
                        if hasattr(module, 'setup'):
                            try:
                                cog = await module.setup(self.bot)
                                if cog is not None:
                                    self.bot.add_cog(cog)
                                    self.loaded_extensions.append(f"{name}.{module_name}")
                                    self.logger.info(f"Loaded event extension: {name}.{module_name}")
                                else:
                                    self.logger.error(f"Setup function returned None for {name}.{module_name}")
                            except Exception as e:
                                self.logger.error(f"Error in setup function for {name}.{module_name}: {e}", exc_info=True)
                    except Exception as e:
                        self.logger.error(f"Failed to load extension {module_name}: {e}", exc_info=True)
            else:
                # Load single module
                try:
                    module = importlib.import_module(f"aurorabot.events.{name}")
                    if hasattr(module, 'setup'):
                        try:
                            cog = await module.setup(self.bot)
                            if cog is not None:
                                self.bot.add_cog(cog)
                                self.loaded_extensions.append(name)
                                self.logger.info(f"Loaded event extension: {name}")
                            else:
                                self.logger.error(f"Setup function returned None for {name}")
                        except Exception as e:
                            self.logger.error(f"Error in setup function for {name}: {e}", exc_info=True)
                except Exception as e:
                    self.logger.error(f"Failed to load event module {name}: {e}", exc_info=True)
                    
    async def reload_extension(self, extension_name: str) -> bool:
        """Reload a specific extension."""
        try:
            module = importlib.import_module(f"aurorabot.{extension_name}")
            if hasattr(module, 'setup'):
                try:
                    cog = await module.setup(self.bot)
                    if cog is not None:
                        self.bot.add_cog(cog)
                        self.logger.info(f"Reloaded extension: {extension_name}")
                        return True
                    else:
                        self.logger.error(f"Setup function returned None for {extension_name}")
                except Exception as e:
                    self.logger.error(f"Error in setup function for {extension_name}: {e}", exc_info=True)
        except Exception as e:
            self.logger.error(f"Failed to reload extension {extension_name}: {e}", exc_info=True)
        return False
            
    def unload_extension(self, extension_name: str) -> bool:
        """Unload a specific extension."""
        try:
            module = importlib.import_module(f"aurorabot.{extension_name}")
            if hasattr(module, 'setup'):
                # Find and remove the cog
                for cog_name, cog in self.bot.cogs.items():
                    if cog.__module__ == f"aurorabot.{extension_name}":
                        self.bot.remove_cog(cog_name)
                        break
                if extension_name in self.loaded_extensions:
                    self.loaded_extensions.remove(extension_name)
                self.logger.info(f"Unloaded extension: {extension_name}")
                return True
        except Exception as e:
            self.logger.error(f"Failed to unload extension {extension_name}: {e}", exc_info=True)
            return False
            
    def get_loaded_extensions(self) -> List[str]:
        """Get a list of loaded extensions."""
        return self.loaded_extensions.copy()

    def load_extensions_from_directory(self) -> None:
        """Загрузка всех расширений (когов) из директории commands."""
        commands_path = self.base_path / "commands"
        if not commands_path.exists():
            self.logger.warning("Директория commands не найдена")
            return

        self.logger.info(f"Поиск команд в директории: {commands_path}")
        
        # Загрузка всех модулей в директории commands
        for _, name, is_pkg in pkgutil.iter_modules([str(commands_path)]):
            self.logger.info(f"Найден модуль/пакет: {name} (is_pkg: {is_pkg})")
            try:
                if is_pkg:
                    # Загрузка пакета
                    package = importlib.import_module(f"aurorabot.commands.{name}")
                    self.logger.info(f"Загружен пакет: aurorabot.commands.{name}")
                    
                    # Поиск и загрузка всех модулей в пакете
                    package_path = commands_path / name
                    self.logger.info(f"Поиск модулей в пакете: {package_path}")
                    
                    for _, module_name, _ in pkgutil.iter_modules([str(package_path)]):
                        self.logger.info(f"Найден модуль в пакете: {module_name}")
                        try:
                            # Загружаем расширение
                            extension_name = f"aurorabot.commands.{name}.{module_name}"
                            self.bot.load_extension(extension_name)
                            self.logger.info(f"Загружено расширение: {extension_name}")
                        except Exception as e:
                            self.logger.error(f"Ошибка при загрузке расширения {module_name}: {e}", exc_info=True)
                else:
                    # Загрузка одиночного модуля
                    try:
                        extension_name = f"aurorabot.commands.{name}"
                        self.bot.load_extension(extension_name)
                        self.logger.info(f"Загружено расширение: {extension_name}")
                    except Exception as e:
                        self.logger.error(f"Ошибка при загрузке модуля {name}: {e}", exc_info=True)
            except Exception as e:
                self.logger.error(f"Ошибка при загрузке {name}: {e}", exc_info=True)

        # Синхронизация команд после загрузки всех расширений
        try:
            self.logger.info("Начало синхронизации команд...")
            synced = self.bot.sync_application_commands()
            if synced is not None:
                self.logger.info(f"Синхронизировано {len(synced)} команд")
            else:
                self.logger.warning("Синхронизация команд вернула None")
        except Exception as e:
            self.logger.error(f"Ошибка при синхронизации команд: {e}", exc_info=True)

    def load_events_from_directory(self) -> None:
        """Загрузка всех обработчиков событий из директории events."""
        events_path = self.base_path / "events"
        if not events_path.exists():
            self.logger.warning("Директория events не найдена")
            return

        # Загружаем обработчики событий
        for _, name, is_pkg in pkgutil.iter_modules([str(events_path)]):
            if is_pkg:
                try:
                    # Загрузка пакета
                    package = importlib.import_module(f"aurorabot.events.{name}")
                    # Поиск и загрузка всех модулей в пакете
                    for _, module_name, _ in pkgutil.iter_modules([str(events_path / name)]):
                        try:
                            extension_name = f"aurorabot.events.{name}.{module_name}"
                            self.bot.load_extension(extension_name)
                            self.logger.info(f"Загружен обработчик событий: {extension_name}")
                        except Exception as e:
                            self.logger.error(f"Ошибка при загрузке обработчика событий {module_name}: {e}")
                except Exception as e:
                    self.logger.error(f"Ошибка при загрузке пакета событий {name}: {e}") 