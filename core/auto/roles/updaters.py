import sqlite3
import nextcord

from ...db_utils import execute_update

async def set_autoroles_state(guild_id: int, autoroles_enabled: bool) -> None:
    sql = "UPDATE autoroles SET autoroles_enabled = %s WHERE guild_id = %s"
    values = (autoroles_enabled, guild_id)
    await execute_update(sql, values)
    return


async def update_autorole(guild_id: int, role_id: int) -> None:
    sql = "UPDATE autoroles SET autorole_id = %s WHERE guild_id = %s"
    values = (role_id, guild_id)
    await execute_update(sql, values)
    return


async def write_autorole_for_level(guild_id: int, role: nextcord.Role, level: int) -> None:
    sql = "INSERT INTO autoroles_level(guild_id, level, autorole_id) VALUES (%s, %s, %s)"
    val = (guild_id, level, role.id)
    await execute_update(sql, val)


async def update_autorole_for_level(guild_id: int, role: nextcord.Role, level: int) -> None:
    sql = "UPDATE autoroles_level SET autorole_id = %s WHERE guild_id = %s AND level = %s"
    val = (role.id, guild_id, level)
    await execute_update(sql, val)


async def update_autorole_on_marriage(guild_id: int, role: nextcord.Role) -> None:
    sql = "UPDATE autoroles_marriage SET autorole_id = %s WHERE guild_id = %s"
    val = (role.id, guild_id)
    await execute_update(sql, val)


async def delete_autorole_for_level(guild_id: int, level: int) -> None:
    sql = f"DELETE FROM autoroles_level WHERE guild_id = {guild_id} AND level = {level}"
    await execute_update(sql)


async def write_autorole_for_reaction(
    guild_id: int,
    channel_id: int,
    message_id: int,
    reaction: str,
    role: nextcord.Role,
    is_custom: bool,
) -> None:
    sql = "INSERT INTO reaction_autorole (guild_id, channel_id, message_id, reaction, autorole_id, is_custom) VALUES " \
          "(%s, %s, %s, %s, %s, %s) "
    val = (guild_id, channel_id, message_id, reaction, role.id, is_custom)
    await execute_update(sql, val)


async def delete_autorole_for_reaction(guild_id: int, role: nextcord.Role) -> None:
    sql = f"DELETE FROM reaction_autorole WHERE guild_id = {guild_id} AND autorole_id = {role.id}"
    await execute_update(sql)


async def update_autorole_lvl_deletion_state(guild_id: int, enabled: bool) -> None:
    sql = "UPDATE autorole_bool SET remove_lvl_roles = %s WHERE guild_id = %s"
    val = (enabled, guild_id)
    await execute_update(sql, val)
