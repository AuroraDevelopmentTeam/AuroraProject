import psutil
import nextcord
from nextcord.ext import commands
from typing import List, Any
from aurorabot.core.base.information import BaseInformationCommand
from aurorabot.core.embeds.builder import EmbedBuilder
from aurorabot.core.embeds.fields import FieldManager


class BotCommand(BaseInformationCommand):
    def __init__(self, bot: commands.Bot):
        super().__init__(bot)

    async def gather_information(self, **kwargs) -> dict:
        """Gather bot information."""
        return {
            'name': self.bot.user.name,
            'avatar': self.bot.user.avatar.url,
            'user_count': len(self.bot.users),
            'guild_count': len(self.bot.guilds),
            'id': self.bot.user.id,
            'cpu_usage': psutil.cpu_percent(),
            'memory_usage': psutil.virtual_memory().percent,
            'memory_available': round((psutil.virtual_memory().available * 100 / psutil.virtual_memory().total), 1),
            'shard_id': kwargs.get('guild', self.bot.guilds[0]).shard_id,
            'status': self.bot.status,
            'created_at': self.bot.user.created_at,
            'python_version': 'Python 3.10.4',
            'library': 'Nextcord',
            'github': 'https://github.com/AuroraDevelopmentTeam'
        }

    async def create_embed(self, ctx: commands.Context, **kwargs) -> nextcord.Embed:
        """Create the bot information embed."""
        info = await self.gather_information(guild=ctx.guild)
        
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
        
        embed = (
            EmbedBuilder(f"{info['name']}:", color=nextcord.Color.blue())
            .with_thumbnail(info['avatar'])
            .with_footer(f"Requested by {ctx.author}", ctx.author.display_avatar)
            .build()
        )
        
        return FieldManager.add_fields(embed, fields)

    @commands.command(name="about")
    async def about(self, ctx: commands.Context) -> None:
        """Display information about the bot."""
        await self.send_embed(ctx)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(BotCommand(bot)) 