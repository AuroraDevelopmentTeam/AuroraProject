import nextcord
from nextcord.ext import commands
from typing import List, Any, Optional
from aurorabot.core.base.information import BaseInformationCommand
from aurorabot.core.embeds.builder import EmbedBuilder
from aurorabot.core.embeds.fields import FieldManager


class UserCommand(BaseInformationCommand):
    def __init__(self, bot: commands.Bot):
        super().__init__(bot)

    async def gather_information(self, **kwargs) -> dict:
        """Gather user information."""
        user = kwargs.get('user')
        if not user:
            return {}

        try:
            activity = user.activity.name
        except AttributeError:
            activity = user.activity

        return {
            'name': user.name,
            'avatar': user.avatar,
            'created_at': user.created_at,
            'discriminator': user.discriminator,
            'joined_at': user.joined_at,
            'desktop_status': user.desktop_status,
            'web_status': user.web_status,
            'mobile_status': user.mobile_status,
            'id': user.id,
            'nick': user.nick,
            'role_count': len(user.roles),
            'activity': activity
        }

    async def create_embed(self, ctx: commands.Context, **kwargs) -> nextcord.Embed:
        """Create the user information embed."""
        user = kwargs.get('user', ctx.author)
        info = await self.gather_information(user=user)
        
        fields = {
            "Created At": nextcord.utils.format_dt(info['created_at']),
            "Discriminator": f"#{info['discriminator']}",
            "Joined At": nextcord.utils.format_dt(info['joined_at']),
            "Desktop Status": info['desktop_status'],
            "Web Status": info['web_status'],
            "Mobile Status": info['mobile_status'],
            "User ID": info['id'],
            "Nickname": info['nick'] or "None",
            "Role Count": info['role_count'],
            "Activity": info['activity'] or "None"
        }
        
        embed = (
            EmbedBuilder(f"{info['name']}:", color=nextcord.Color.blue())
            .with_thumbnail(info['avatar'])
            .with_footer(f"Requested by {ctx.author}", ctx.author.display_avatar)
            .build()
        )
        
        return FieldManager.add_fields(embed, fields)

    @commands.command(name="user")
    async def user(self, ctx: commands.Context, member: Optional[nextcord.Member] = None) -> None:
        """Display information about a user."""
        await self.send_embed(ctx, user=member or ctx.author)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(UserCommand(bot)) 