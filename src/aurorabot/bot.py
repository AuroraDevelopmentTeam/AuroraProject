from typing import Optional
import nextcord
from nextcord.ext import commands
from aurorabot.config.config import Config
from aurorabot.loader.extension_loader import ExtensionLoader


class AuroraBot(commands.Bot):
    def __init__(self):
        # Писать комментарии это хорошо, поэтому
        # Загрузка конфигурации
        self.config = Config()
        
        # Интенты ботяры, QUESTION: это все которые нам нужны?
        intents = nextcord.Intents.default()
        intent_mapping = {
            "GUILDS": "guilds",
            "GUILD_MESSAGES": "guild_messages",
            "GUILD_MEMBERS": "members",
            "MESSAGE_CONTENT": "message_content",
            "GUILD_PRESENCES": "presences",
            "GUILD_VOICE_STATES": "voice_states"
        }
        
        for intent in self.config.bot_config["intents"]:
            if intent in intent_mapping:
                setattr(intents, intent_mapping[intent], True)
            else:
                self.config.logger.warning(f"Неизвестный интент: {intent}")

        # Инициализация бота
        super().__init__(
            command_prefix=self.config.bot_config["prefix"],
            intents=intents,
            case_insensitive=True,
            help_command=None  # Мы реализуем свою команду помощи
        )

        self.logger = self.config.logger
        self.logger.info("AuroraBot инициализирован")

    async def setup_hook(self) -> None:
        """Инициализация компонентов бота и загрузка расширений."""
        self.logger.info("Настройка компонентов бота...")
        
        # Инициализация загрузчика расширений
        loader = ExtensionLoader(self, self.logger)
        
        # Загрузка всех когов и событий
        await loader.load_extensions()
        await loader.load_events()
        
        self.logger.info("Настройка бота завершена")

    async def on_ready(self) -> None:
        """Вызывается, когда бот готов к работе."""
        self.logger.info(f"Вошли как {self.user} (ID: {self.user.id})")
        await self.change_presence(
            activity=nextcord.Game(name=f"{self.config.bot_config['prefix']}help | v{self.config.bot_config['version']}")
        )

    async def on_command_error(self, ctx: commands.Context, error: Exception) -> None: # Это надо будет вынести в отдельный блок
        """Глобальный обработчик ошибок команд."""
        if isinstance(error, commands.CommandNotFound):
            return
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send("У вас нет прав для использования этой команды.")
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"Отсутствует обязательный аргумент: {error.param.name}")
        else:
            self.logger.error(f"Ошибка команды: {error}", exc_info=True)
            await ctx.send("Произошла ошибка при обработке команды.")
