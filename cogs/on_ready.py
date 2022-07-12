from nextcord.ext import commands
import sqlite3
from core.locales import *
from core.checkers import is_guild_id_in_table


class OnReadyListener(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        create_locales_table()
        write_in_locales_standart_values(self.client.guilds)


def setup(client):
    client.add_cog(OnReadyListener(client))
