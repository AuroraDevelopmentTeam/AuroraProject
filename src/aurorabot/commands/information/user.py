import nextcord
from nextcord.ext import commands
from typing import Dict, Any, Optional, List
from aurorabot.core.base.information import BaseInformationCommand
from aurorabot.core.services.embed_service import EmbedService
from aurorabot.core.services.locale_service import LocaleService


class UserCommand(BaseInformationCommand):
    """Command for displaying user information."""
    
    def __init__(self, bot: commands.Bot) -> None:
        """Initialize the user command.
        
        Args:
            bot: The bot instance
        """
        super().__init__(bot)
        self.embed_service = EmbedService()
        self.logger = bot.logger
        self._field_mappings = {
            'id': lambda info: info['id'],
            'created_at': lambda info: self.locale_service.get_text("commands.user.fields.created_at", date=info['created_at']),
            'joined_at': lambda info: self.locale_service.get_text("commands.user.fields.joined_at", date=info['joined_at']),
            'roles': lambda info: self.locale_service.get_text("commands.user.fields.roles", roles=info['roles']),
            'top_role': lambda info: self.locale_service.get_text("commands.user.fields.top_role", role=info['top_role']),
            'status': lambda info: self.locale_service.get_text("commands.user.fields.status", status=info['status']),
            'activity': lambda info: self.locale_service.get_text("commands.user.fields.activity", activity=info.get('activities', [None])[0] if info.get('activities') else None)
        }

    @nextcord.slash_command(
        name="user",
        description="Display information about a user",
        **LocaleService.get_command_localizations("user")
    )
    async def user(self, interaction: nextcord.Interaction, member: nextcord.Member = None) -> None:
        """Display information about a user.
        
        Args:
            interaction: The interaction that triggered the command
            member: The member to get information about (defaults to the command user)
        """
        await self.execute(interaction, user=member or interaction.user)

    async def gather_information(self, **kwargs) -> Dict[str, Any]:
        """Gather user information.
        
        Args:
            **kwargs: Additional arguments containing the user
            
        Returns:
            Dict[str, Any]: The gathered user information
            
        Raises:
            ValueError: If no user is provided
        """
        user = kwargs.get('user')
        if not user:
            raise ValueError("User is required for user information")
            
        return {
            'name': user.name,
            'id': user.id,
            'avatar': user.avatar.url if user.avatar else None,
            'created_at': user.created_at,
            'joined_at': user.joined_at if hasattr(user, 'joined_at') else None,
            'roles': [role for role in user.roles if role.name != "@everyone"],
            'top_role': user.top_role,
            'color': user.color,
            'is_bot': user.bot,
            'nickname': user.nick,
            'status': user.status,
            'activities': user.activities,
            'banner': user.banner.url if user.banner else None
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
            self.locale_service.get_text(f"commands.user.fields.{key}"): self._get_field_value(key, info)
            for key in self._field_mappings
        }
        
        if info['roles']:
            fields[self.locale_service.get_text("commands.user.fields.roles")] = ", ".join([role.mention for role in info['roles']])
            
        return fields

    async def create_embed(self, interaction: nextcord.Interaction, **kwargs) -> nextcord.Embed:
        """Create the user information embed.
        
        Args:
            interaction: The interaction that triggered the command
            **kwargs: Additional arguments
            
        Returns:
            nextcord.Embed: The created embed
        """
        info = await self.gather_information(user=kwargs.get('user', interaction.user))
        
        embed = self.embed_service.create_embed(
            title=self.locale_service.get_text("commands.user.title", name=info['name']),
            color=info['color'] or nextcord.Color.blue(),
            thumbnail=info['avatar'],
            footer_text=self.locale_service.get_text("common.requested_by", user=str(interaction.user)),
            footer_icon=interaction.user.display_avatar.url
        )
        
        if info['banner']:
            embed.set_image(url=info['banner'])
            
        return self.embed_service.add_fields(embed, self._get_fields(info))


async def setup(bot: commands.Bot) -> UserCommand:
    """Setup the cog.
    
    Args:
        bot: The bot instance
        
    Returns:
        UserCommand: The loaded cog
    """
    bot.logger.info("Loading UserCommand cog...")
    cog = UserCommand(bot)
    bot.logger.info("UserCommand cog loaded successfully")
    return cog 