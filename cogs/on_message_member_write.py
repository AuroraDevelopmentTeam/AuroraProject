import nextcord
from nextcord.ext import commands
import sqlite3
from core.locales.create import create_locales_table
from core.locales.writers import write_in_locales_standart_values
from core.checkers import is_guild_id_in_table
from core.money.create import create_money_table, create_money_config_table
from core.money.writers import (
    write_in_money_standart_values,
    write_in_money_config_standart_values,
)
from core.levels.create import create_level_table, create_level_config_table
from core.levels.writers import (
    write_in_levels_standart_values,
    write_in_levels_config_standart_values,
)
from core.welcomers.create import create_welcomers_config
from core.welcomers.writers import write_in_welcomers_config_standart_values
from core.warns.create import create_warns_table
from core.auto.roles.create import create_autoroles_table
from core.auto.roles.writers import write_in_autoroles_standart_values
from core.marriage.create import create_marriage_table, create_gifts_table
from core.marriage.writers import (
    write_in_marriage_standart_values,
    write_in_gifts_standart_values,
)
from core.shop.create import create_shop_table
from core.goodbyes.create import create_goodbye_config
from core.goodbyes.writers import write_in_goodbye_config_standart_values
from core.nitro.create import create_on_nitro_config
from core.nitro.writers import write_in_on_nitro_config_standart_values
from core.honor.create import create_honor_table
from core.honor.writers import write_in_honor_standart_values
from core.profiles.create import create_profiles_table
from core.profiles.writers import write_in_profiles_standart_values
from core.stats.create import create_stats_table
from core.stats.writers import write_in_stats_standart_values
from core.badges.create import create_badges_table
from core.badges.writers import write_in_badges_standart_values
from core.loggers.create import create_loggers_table
from core.loggers.writers import write_in_loggers_standart_values
from core.tickets.create import create_tickets_config_table
from core.tickets.writers import write_in_tickets_config_standart_values
from core.utils import (
    write_member_in_gifts,
    write_member_in_badges,
    write_member_in_levels,
    write_member_in_marriage,
    write_member_in_profiles,
    write_member_in_stats,
    write_member_in_honor,
    write_member_in_money,
    write_member_in_clan,
)
from core.checkers import is_user_in_table


class OnMessageListener(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message: nextcord.Message):
        guild = message.guild
        member = message.author
        if not message.author.bot:
            if await is_user_in_table("money", guild.id, member.id) is False:
                await write_member_in_money(guild, member)
                await write_member_in_levels(guild, member)
                await write_member_in_profiles(guild, member)
                await write_member_in_marriage(guild, member)
                await write_member_in_gifts(guild, member)
                await write_member_in_honor(member)
                await write_member_in_profiles(guild, member)
                await write_member_in_stats(guild, member)
                await write_member_in_badges(guild, member)
                await write_member_in_clan(guild, member)
            else:
                return


def setup(client):
    client.add_cog(OnMessageListener(client))
