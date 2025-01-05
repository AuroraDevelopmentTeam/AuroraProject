import sqlite3
from core.checkers import is_guild_id_in_table, is_user_in_table

from ...db_utils import execute_update

async def write_in_autoroles_standart_values(guilds) -> None:
    for guild in guilds:
        if await is_guild_id_in_table("autoroles", guild.id) is False:
            sql = (
                "INSERT INTO autoroles(guild_id, autoroles_enabled, "
                "autorole_id) VALUES (%s, %s, %s)"
            )
            val = (guild.id, True, 0)
            await execute_update(sql, val)


async def write_in_levelroles_value(guild_id, level, role_id):
    sql = "INSERT INTO autoroles_level(guild_id, level, autorole_id) VALUES (%s, %s, %s)"
    val = (guild_id, level, role_id)
    await execute_update(sql, val)


async def write_in_autoroles_bool_standart_values(guilds) -> None:
    for guild in guilds:
        if await is_guild_id_in_table("autorole_bool", guild.id) is False:
            sql = (
                "INSERT INTO autorole_bool(guild_id, remove_lvl_roles) VALUES (%s, %s)"
            )
            val = (guild.id, False)
            await execute_update(sql, val)


async def write_in_autoroles_marriage_standart_values(guilds) -> None:
    for guild in guilds:
        if await is_guild_id_in_table("autoroles_marriage", guild.id) is False:
            sql = (
                "INSERT INTO autoroles_marriage(guild_id, autorole_id) VALUES (%s, %s)"
            )
            val = (guild.id, 0)
            await execute_update(sql, val)
