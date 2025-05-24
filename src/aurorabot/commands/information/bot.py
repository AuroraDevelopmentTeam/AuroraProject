import psutil
import nextcord
from nextcord.ext import commands
from typing import Dict, Any
from aurorabot.core.base.information import BaseInformationCommand
from aurorabot.core.services.embed_service import EmbedService


class BotCommand(BaseInformationCommand):
    """Command for displaying bot information."""
    
    def __init__(self, bot: commands.Bot):
        super().__init__(bot)

    @nextcord.slash_command(
        name="about",
        description="Display information about the bot"
    )
    async def about(self, interaction: nextcord.Interaction) -> None:
        """Display information about the bot."""
        await self.execute(interaction)

    async def gather_information(self, **kwargs) -> Dict[str, Any]:
        """Gather bot information."""
        guild = kwargs.get('guild', self.bot.guilds[0])
        return {
            'name': self.bot.user.name,
            'avatar': self.bot.user.avatar.url,
            'user_count': len(self.bot.users),
            'guild_count': len(self.bot.guilds),
            'id': self.bot.user.id,
            'cpu_usage': psutil.cpu_percent(),
            'memory_usage': psutil.virtual_memory().percent,
            'memory_available': round((psutil.virtual_memory().available * 100 / psutil.virtual_memory().total), 1),
            'shard_id': guild.shard_id,
            'status': self.bot.status,
            'created_at': self.bot.user.created_at,
            'python_version': 'Python 3.10.4',
            'library': 'Nextcord',
            'github': 'https://github.com/AuroraDevelopmentTeam'
        }

    async def create_embed(self, interaction: nextcord.Interaction, **kwargs) -> nextcord.Embed:
        """Create the bot information embed."""
        info = await self.gather_information(guild=interaction.guild)
        
        fields = {
            "Users": f"{info['user_count']} 🧍",
            "Servers": info['guild_count'],
            "Bot ID": info['id'],
            "CPU Usage": f"{info['cpu_usage']}%",
            "Memory Usage": f"{info['memory_usage']}%",
            "Memory Available": f"{info['memory_available']}%",
            "Shard ID": info['shard_id'],
            "Status": info['status'],
            "Created At": nextcord.utils.format_dt(info['created_at']),
            "Python Version": info['python_version'],
            "Library": info['library'],
            "GitHub": info['github']
        }
        
        embed = self.embed_service.create_embed(
            title=f"{info['name']}:",
            color=nextcord.Color.blue(),
            thumbnail=info['avatar'],
            footer_text=f"Requested by {interaction.user}",
            footer_icon=interaction.user.display_avatar.url
        )
        
        return self.embed_service.add_fields(embed, fields)


async def setup(bot: commands.Bot) -> BotCommand:
    """Установка кога."""
    bot.logger.info("Загрузка кога BotCommand...")
    cog = BotCommand(bot)
    bot.logger.info("Ког BotCommand успешно загружен")
    return cog 