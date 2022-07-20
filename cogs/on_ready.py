from nextcord.ext import commands
import sqlite3
from core.locales.create import create_locales_table
from core.locales.writers import write_in_locales_standart_values
from core.checkers import is_guild_id_in_table
from core.money.create import create_money_table, create_money_config_table
from core.money.writers import write_in_money_standart_values, write_in_money_config_standart_values
from core.levels.create import create_level_table, create_level_config_table
from core.levels.writers import write_in_levels_standart_values, write_in_levels_config_standart_values
from core.welcomers.create import create_welcomers_config
from core.welcomers.writers import write_in_welcomers_config_standart_values
from core.warns.create import create_warns_table


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
        create_level_config_table()
        create_level_table()
        write_in_levels_config_standart_values(self.client.guilds)
        write_in_levels_standart_values(self.client.guilds)
        create_welcomers_config()
        write_in_welcomers_config_standart_values(self.client.guilds)
        create_warns_table()


def setup(client):
    client.add_cog(OnReadyListener(client))
