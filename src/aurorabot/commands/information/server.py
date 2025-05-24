import nextcord
from nextcord.ext import commands
from typing import Dict, Any, Optional, List
from src.aurorabot.core.base.information import BaseInformationCommand
from aurorabot.core.services.embed_service import EmbedService
from aurorabot.core.services.locale_service import LocaleService


class ServerCommand(BaseInformationCommand):
    """Command for displaying server information."""
    
    def __init__(self, bot: commands.Bot) -> None:
        """Initialize the server command.
        
        Args:
            bot: The bot instance
        """
        super().__init__(bot)
        self._field_mappings = {
            'id': lambda info: info['id'],
            'created_at': lambda info: self.locale_service.get_text("commands.server.fields.created_at", date=info['created_at']),
            'owner': lambda info: self.locale_service.get_text("commands.server.fields.owner", owner=info['owner']),
            'members': lambda info: self.locale_service.get_text("commands.server.fields.members", count=info['member_count']),
            'channels': lambda info: self.locale_service.get_text("commands.server.fields.channels", count=info['channel_count']),
            'roles': lambda info: self.locale_service.get_text("commands.server.fields.roles", count=info['role_count']),
            'boost_level': lambda info: self.locale_service.get_text("commands.server.fields.boost_level", level=info['boost_level']),
            'verification_level': lambda info: self.locale_service.get_text("commands.server.fields.verification_level", level=info['verification_level'])
        }

    @nextcord.slash_command(
        name="server",
        description="Display information about the server",
        **LocaleService.get_command_localizations("server")
    )
    async def server(self, interaction: nextcord.Interaction) -> None:
        """Display information about the server.
        
        Args:
            interaction: The interaction that triggered the command
        """
        await self.execute(interaction, guild=interaction.guild)

    async def gather_information(self, **kwargs) -> Dict[str, Any]:
        """Gather server information.
        
        Args:
            **kwargs: Additional arguments
            
        Returns:
            Dict[str, Any]: The gathered server information
        """
        guild = kwargs.get('guild')
        if not guild:
            raise ValueError("Guild is required for server information")
            
        return {
            'name': guild.name,
            'id': guild.id,
            'icon': guild.icon.url if guild.icon else None,
            'banner': guild.banner.url if guild.banner else None,
            'splash': guild.splash.url if guild.splash else None,
            'created_at': guild.created_at,
            'owner': guild.owner,
            'member_count': guild.member_count,
            'channel_count': len(guild.channels),
            'role_count': len(guild.roles),
            'boost_level': guild.premium_tier,
            'verification_level': guild.verification_level,
            'explicit_content_filter': guild.explicit_content_filter,
            'mfa_level': guild.mfa_level,
            'premium_tier': guild.premium_tier,
            'premium_subscription_count': guild.premium_subscription_count,
            'description': guild.description,
            'features': guild.features
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
        fields = {
            self.locale_service.get_text(f"commands.server.fields.{key}"): self._get_field_value(key, info)
            for key in self._field_mappings
        }
        
        if info['features']:
            fields[self.locale_service.get_text("commands.server.fields.features")] = ", ".join(info['features'])
            
        return fields

    async def create_embed(self, interaction: nextcord.Interaction, **kwargs) -> nextcord.Embed:
        """Create the server information embed.
        
        Args:
            interaction: The interaction that triggered the command
            **kwargs: Additional arguments
            
        Returns:
            nextcord.Embed: The created embed
        """
        info = kwargs.get('info', await self.gather_information(**kwargs))
        
        embed = self.embed_service.create_embed(
            title=self.locale_service.get_text("commands.server.title", name=info['name']),
            color=nextcord.Color.blue(),
            thumbnail=info['icon'],
            footer_text=self.locale_service.get_text("common.requested_by", user=str(interaction.user)),
            footer_icon=interaction.user.display_avatar.url
        )
        
        if info['banner']:
            embed.set_image(url=info['banner'])
            
        if info['description']:
            embed.description = info['description']
            
        return self.embed_service.add_fields(embed, self._get_fields(info))


async def setup(bot: commands.Bot) -> ServerCommand:
    """Setup the cog.
    
    Args:
        bot: The bot instance
        
    Returns:
        ServerCommand: The loaded cog
    """
    bot.logger.info("Loading ServerCommand cog...")
    cog = ServerCommand(bot)
    bot.logger.info("ServerCommand cog loaded successfully")
    return cog 