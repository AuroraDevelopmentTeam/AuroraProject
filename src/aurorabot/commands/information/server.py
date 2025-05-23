import nextcord
from nextcord.ext import commands
from typing import List, Any
from aurorabot.core.base.information import BaseInformationCommand
from aurorabot.core.embeds.builder import EmbedBuilder
from aurorabot.core.embeds.fields import FieldManager


class ServerCommand(BaseInformationCommand):
    def __init__(self, bot: commands.Bot):
        super().__init__(bot)

    async def gather_information(self, **kwargs) -> dict:
        """Gather server information."""
        guild = kwargs.get('guild')
        if not guild:
            return {}

        return {
            'name': guild.name,
            'icon': guild.icon or f"https://ui-avatars.com/api/?name={guild.name.replace(' ', '+')}",
            'member_count': guild.member_count,
            'owner': await self.bot.fetch_user(guild.owner_id),
            'emoji_count': len(guild.emojis),
            'created_at': guild.created_at,
            'id': guild.id,
            'channel_count': len(guild.channels),
            'voice_channel_count': len(guild.voice_channels),
            'text_channel_count': len(guild.text_channels),
            'category_count': len(guild.categories),
            'role_count': len(guild.roles),
            'shard_id': guild.shard_id,
            'content_filter': guild.explicit_content_filter,
            'description': guild.description,
            'premium_tier': guild.premium_tier,
            'premium_subscription_count': guild.premium_subscription_count
        }

    async def create_embed(self, ctx: commands.Context, **kwargs) -> nextcord.Embed:
        """Create the server information embed."""
        info = await self.gather_information(guild=ctx.guild)
        
        fields = {
            "Members": f"{info['member_count']} 🧍",
            "Owner": info['owner'],
            "Emojis": info['emoji_count'],
            "Created At": info['created_at'].strftime('%a, %d %b %Y'),
            "Server ID": info['id'],
            "Total Channels": info['channel_count'],
            "Voice Channels": info['voice_channel_count'],
            "Text Channels": info['text_channel_count'],
            "Categories": info['category_count'],
            "Roles": info['role_count'],
            "Shard ID": info['shard_id'],
            "Content Filter": info['content_filter'],
            "Description": info['description'] or "No description",
            "Boost Tier": info['premium_tier'],
            "Boost Count": info['premium_subscription_count']
        }
        
        embed = (
            EmbedBuilder(f"{info['name']}:", color=nextcord.Color.blue())
            .with_thumbnail(info['icon'])
            .with_footer(f"Requested by {ctx.author}", ctx.author.display_avatar)
            .build()
        )
        
        return FieldManager.add_fields(embed, fields)

    @commands.command(name="server")
    async def server(self, ctx: commands.Context) -> None:
        """Display information about the server."""
        await self.send_embed(ctx)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(ServerCommand(bot)) 