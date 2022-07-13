from nextcord.ext import commands
import sqlite3
from core.locales.create import create_locales_table
from core.locales.writers import write_in_locales_standart_values
from core.checkers import is_guild_id_in_table
from core.money import create_money_table, create_money_config_table, \
    write_in_money_config_standart_values, write_in_money_standart_values


class OnReadyListener(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        create_locales_table()
        write_in_locales_standart_values(self.client.guilds)
        create_money_config_table()
        create_money_table()
        write_in_money_config_standart_values(self.client.guilds)
        write_in_money_standart_values(self.client.guilds)


def setup(client):
    client.add_cog(OnReadyListener(client))
