from typing import Optional
import nextcord
from nextcord.ext import commands
from aurorabot.core.services.logger_service import LoggerService
from aurorabot.core.services.config_service import ConfigService
from aurorabot.core.services.embed_service import EmbedService
from aurorabot.core.services.error_handler_service import ErrorHandlerService
from aurorabot.core.services.locale_service import LocaleService


class AuroraBot(commands.Bot):
    """Main bot class."""
    
    def __init__(self):
        # Initialize logger first
        self.logger = LoggerService().get_logger()
        
        # Initialize other services
        self.config = ConfigService().load_config()
        self.embed_service = EmbedService()
        self.error_handler = ErrorHandlerService(self.logger)
        self.locale_service = LocaleService(self.logger)
        
        # Initialize bot with intents
        intents = nextcord.Intents.default()
        intents.message_content = True
        intents.members = True
        
        # Get application ID from config
        application_id = self.config.get("bot.application_id")
        if not application_id:
            self.logger.error("Application ID not found in configuration")
            raise ValueError("Application ID is required for slash commands")
            
        self.logger.info(f"Using application ID: {application_id}")
        
        # Set intents from config
        config_intents = self.config.get("bot.intents", [])
        for intent in config_intents:
            if hasattr(intents, intent.lower()):
                setattr(intents, intent.lower(), True)
                self.logger.info(f"Enabled intent: {intent}")
        
        super().__init__(
            command_prefix=self.config.get("bot.prefix", "!"),
            intents=intents,
            help_command=None,
            application_id=int(application_id)
        )
        
        self.logger.info("Bot initialized")
        
    async def on_ready(self):
        """Called when the bot is ready."""
        self.logger.info(f"Logged in as {self.user.name}#{self.user.discriminator} (ID: {self.user.id})")
        
        # Load extensions
        from aurorabot.loader.extension_loader import ExtensionLoader
        extension_loader = ExtensionLoader(self)
        
        # Load commands
        await extension_loader.load_extensions()
        
        # Load events
        await extension_loader.load_events()
        
        # Set bot presence
        activity = nextcord.Activity(
            type=nextcord.ActivityType.watching,
            name="for commands"
        )
        await self.change_presence(activity=activity)
        
        self.logger.info("Bot is ready")
        
    async def on_command_error(self, ctx, error):
        """Handle command errors."""
        if isinstance(error, commands.CommandNotFound):
            return
            
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You don't have permission to use this command.")
            return
            
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"Missing required argument: {error.param.name}")
            return
            
        self.logger.error(f"Command error: {error}", exc_info=True)
        await ctx.send("An error occurred while processing the command.")

    async def on_application_command_error(
        self,
        interaction: nextcord.Interaction,
        error: Exception
    ) -> None:
        """Handle slash command errors."""
        self.logger.error(f"Ошибка команды: {error}", exc_info=True)
        
        if isinstance(error, nextcord.errors.InteractionResponded):
            await interaction.followup.send(
                self.locale_service.get_text("common.error.timeout"),
                ephemeral=True
            )
        else:
            await self.error_handler.handle_error(interaction, error)

    async def on_application_command(self, interaction: nextcord.Interaction) -> None:
        """Called when a slash command is used."""
        self.logger.info(f"Использована команда {interaction.application_command.name} пользователем {interaction.user}")

    def run_bot(self):
        """Run the bot."""
        token = self.config.get("bot.token")
        
        if not token:
            self.logger.error("Bot token not found in configuration")
            return
            
        self.run(token, reconnect=True)
