import random
import sqlite3

from core.checkers import is_user_in_table, is_guild_id_in_table
from core.db_utils import execute_update


async def write_in_clan_members_standart_values(guilds) -> None:
    for guild in guilds:
        for member in guild.members:
            if not member.bot:
                if await is_user_in_table("clan_members", guild.id, member.id) is False:
                    sql = "INSERT INTO clan_members(guild_id, user_id, clan_id, join_date) VALUES (%s, %s, %s, %s)"
                    val = (guild.id, member.id, 0, "0")
                    await execute_update(sql, val)


async def write_in_clan_config_standart_values(guilds) -> None:
    for guild in guilds:
        if await is_guild_id_in_table("clan_config", guild.id) is False:
            sql = (
                "INSERT INTO clan_config(guild_id, create_cost, upgrade_attack_cost, "
                "upgrade_limit_cost, change_icon_cost, change_image_cost, upgrade_boss_cost, create_clan_channels, "
                "clan_voice_category, change_color_cost, change_name_cost) VALUES (%s, %s, %s, %s, %s, "
                "%s, %s, %s, %s, %s, %s) "
            )
            val = (guild.id, 100000, 500000, 1000000, 10000, 50000, 250000, True, 0, 50000, 100000)
            await execute_update(sql, val)


async def write_clan(
    guild_id: int,
    owner_id: int,
    create_date: str,
    icon: str,
    clan_description: str,
    clan_name: str,
    clan_role: int,
    clan_voice_channel: int,
    clan_color: str,
) -> None:
    sql = (
        "INSERT INTO clans(guild_id, clan_id, clan_level, clan_exp, owner_id, member_limit, storage, create_date, "
        "icon, image, min_attack, max_attack, guild_boss_level, guild_boss_hp, clan_description, clan_name, "
        "clan_role, clan_voice_channel, clan_color) VALUES "
        "(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) "
    )
    val = (
        guild_id,
        random.randint(1, 999999999999999),
        1,
        0,
        owner_id,
        15,
        0,
        create_date,
        icon,
        "0",
        4,
        9,
        1,
        100,
        clan_description,
        clan_name,
        clan_role,
        clan_voice_channel,
        clan_color,
    )
    await execute_update(sql, val)


async def write_clan_on_start(guild_id: int, owner_id: int) -> None:
    sql = (
        "INSERT INTO clans(guild_id, clan_id, clan_level, clan_exp, owner_id, member_limit, storage, create_date, "
        "icon, image, min_attack, max_attack, guild_boss_level, guild_boss_hp, clan_description, clan_name, "
        "clan_role, clan_voice_channel, clan_color) VALUES "
        "(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) "
    )
    val = (
        guild_id,
        random.randint(1, 999999999999999),
        1,
        0,
        owner_id,
        15,
        0,
        "0",
        "0",
        "0",
        4,
        9,
        1,
        100,
        "0",
        "0",
        "0",
        "0",
        "0",
    )
    await execute_update(sql, val)
