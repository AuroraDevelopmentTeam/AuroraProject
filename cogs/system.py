import nextcord
from nextcord.ext import commands
from config import settings
import sqlite3
from core.locales import update_guild_locale
from core.checkers import is_locale_valid


class System(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['set_locale'])
    async def __set_locale(self, ctx, locale: str):
        if is_locale_valid(locale) is True:
            update_guild_locale(locale, ctx.guild.id)
            await ctx.send('done')
        else:
            await ctx.send('something gone wrong')


def setup(client):
    client.add_cog(System(client))
