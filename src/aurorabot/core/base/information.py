from abc import abstractmethod
import nextcord
from nextcord.ext import commands
from typing import Dict, Any, Optional, Callable
from src.aurorabot.core.services.embed_service import EmbedService
from src.aurorabot.core.services.locale_service import LocaleService


class BaseInformationCommand(commands.Cog):
    """Base class for information commands that display data in embeds."""
    
    def __init__(self, bot: commands.Bot) -> None:
        """Initialize the base information command.
        
        Args:
            bot: The bot instance
        """
        self.bot = bot
        self.logger = bot.logger
        self.embed_service = EmbedService()
        self.locale_service = LocaleService(self.logger)
        self._field_mappings: Dict[str, Callable[[Dict[str, Any]], Any]] = {}

    @abstractmethod
    async def gather_information(self, **kwargs) -> Dict[str, Any]:
        """Gather information for the command.
        
        Returns:
            Dict[str, Any]: The gathered information
        """
        raise NotImplementedError("Subclasses must implement gather_information")

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
            self.locale_service.get_text(f"commands.{self.__class__.__name__.lower().replace('command', '')}.fields.{key}"): self._get_field_value(key, info)
            for key in self._field_mappings
        }

    @abstractmethod
    async def create_embed(self, interaction: nextcord.Interaction, **kwargs) -> nextcord.Embed:
        """Create the embed for the command.
        
        Args:
            interaction: The interaction that triggered the command
            **kwargs: Additional arguments
            
        Returns:
            nextcord.Embed: The created embed
        """
        raise NotImplementedError("Subclasses must implement create_embed")

    @classmethod
    def localized_command(
        cls,
        name_key: str,
        description_key: str,
        **kwargs
    ) -> Callable:
        """Create a localized slash command.
        
        Args:
            name_key: The localization key for the command name
            description_key: The localization key for the command description
            **kwargs: Additional arguments for the slash command
            
        Returns:
            Callable: The decorated command function
        """
        def decorator(func):
            # Create the slash command with localized strings
            return nextcord.slash_command(
                name=name_key,
                description=description_key,
                **kwargs
            )(func)
        return decorator

    async def execute(self, interaction: nextcord.Interaction, **kwargs) -> None:
        """Execute the command.
        
        Args:
            interaction: The interaction that triggered the command
            **kwargs: Additional arguments
        """
        self.logger.info(f"Command {self.__class__.__name__} called by {interaction.user}")
        
        try:
            info = await self.gather_information(**kwargs)
            embed = await self.create_embed(interaction, info=info, **kwargs)
            await interaction.response.send_message(embed=embed)
            self.logger.info(f"Command {self.__class__.__name__} executed successfully for {interaction.user}")
        except Exception as e:
            self.logger.error(f"Error executing command: {e}", exc_info=True)
            await interaction.response.send_message(
                self.locale_service.get_text("common.error.execution", error=str(e)),
                ephemeral=True
            )

    def format_field(self, name: str, value: Any, inline: bool = True) -> Dict[str, Any]:
        """Format a field for the embed.
        
        Args:
            name: The field name
            value: The field value
            inline: Whether the field should be inline
            
        Returns:
            Dict[str, Any]: The formatted field
        """
        return {
            "name": name,
            "value": str(value) if value is not None else "N/A",
            "inline": inline
        }

    def register_localized_command(
        self,
        name_key: str,
        description_key: str,
        **kwargs
    ) -> Callable:
        """Register a localized slash command.
        
        Args:
            name_key: The localization key for the command name
            description_key: The localization key for the command description
            **kwargs: Additional arguments for the slash command
            
        Returns:
            Callable: The decorated command function
        """
        def decorator(func):
            # Get localized name and description
            name = self.locale_service.get_text(name_key)
            description = self.locale_service.get_text(description_key)
            
            # Create the slash command with localized strings
            return nextcord.slash_command(
                name=name,
                description=description,
                **kwargs
            )(func)
        return decorator
