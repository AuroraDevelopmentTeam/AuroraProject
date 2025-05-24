import nextcord
from nextcord.ext import commands
import logging

logger = logging.getLogger("aurorabot")


class Ready(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        """Called when the bot is ready."""
        logger.info(f"Bot is ready! Logged in as {self.bot.user}")
        logger.info(f"Bot is in {len(self.bot.guilds)} guilds")

        # Log all guilds the bot is in
        for guild in self.bot.guilds:
            logger.info(f"Connected to guild: {guild.name} (ID: {guild.id})")

        # Set bot status
        await self.bot.change_presence(
            activity=nextcord.Game(name=f"{self.bot.command_prefix}help | v{self.bot.config['bot']['version']}")
        )


async def setup(bot: commands.Bot) -> Ready:
    """Установка кога."""
    bot.logger.info("Загрузка кога Ready...")
    cog = Ready(bot)
    bot.logger.info("Ког Ready успешно загружен")
    return cog
