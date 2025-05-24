import nextcord
from nextcord.ext import commands
from typing import Dict, Any
from src.aurorabot.core.base.information import BaseInformationCommand
from aurorabot.core.services.embed_service import EmbedService
from aurorabot.core.services.locale_service import LocaleService


class PingCommand(BaseInformationCommand):
    """Command for checking bot latency."""

    def __init__(self, bot: commands.Bot) -> None:
        """Initialize the ping command.
        
        Args:
            bot: The bot instance
        """
        super().__init__(bot)
        self.embed_service = EmbedService()
        self.logger = bot.logger
        self._field_mappings = {
            'bot_latency': lambda info: self.locale_service.get_text("commands.ping.milliseconds", value=info['latency'])
        }

    @nextcord.slash_command(
        name="ping",
        description="Check bot latency",
        **LocaleService.get_command_localizations("ping")
    )
    async def ping(self, interaction: nextcord.Interaction) -> None:
        """Check bot latency.
        
        Args:
            interaction: The interaction that triggered the command
        """
        await self.execute(interaction)

    async def gather_information(self, **kwargs) -> Dict[str, Any]:
        """Gather ping information.
        
        Returns:
            Dict[str, Any]: The gathered ping information
        """
        return {
            'latency': round(self.bot.latency * 1000)
        }

    def _get_field_value(self, field_key: str, info: Dict[str, Any]) -> str:
        """Get the value for a field.
        
        Args:
            field_key: The key of the field
            info: The gathered information
            
        Returns:
            str: The formatted field value
        """
        return str(self._field_mappings[field_key](info))

    def _get_fields(self, info: Dict[str, Any]) -> Dict[str, str]:
        """Get all fields for the embed.
        
        Args:
            info: The gathered information
            
        Returns:
            Dict[str, str]: The fields for the embed
        """
        return {
            self.locale_service.get_text(f"commands.ping.{key}"): self._get_field_value(key, info)
            for key in self._field_mappings
        }

    async def create_embed(self, interaction: nextcord.Interaction, **kwargs) -> nextcord.Embed:
        """Create the ping information embed.
        
        Args:
            interaction: The interaction that triggered the command
            **kwargs: Additional arguments
            
        Returns:
            nextcord.Embed: The created embed
        """
        info = await self.gather_information()
        
        embed = self.embed_service.create_embed(
            title=self.locale_service.get_text("commands.ping.title"),
            color=nextcord.Color.green(),
            footer_text=self.locale_service.get_text("common.requested_by", user=str(interaction.user)),
            footer_icon=interaction.user.display_avatar.url
        )
        
        return self.embed_service.add_fields(embed, self._get_fields(info))


async def setup(bot: commands.Bot) -> PingCommand:
    """Setup the cog.
    
    Args:
        bot: The bot instance
        
    Returns:
        PingCommand: The loaded cog
    """
    bot.logger.info("Loading PingCommand cog...")
    cog = PingCommand(bot)
    bot.logger.info("PingCommand cog loaded successfully")
    return cog 