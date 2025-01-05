import sqlite3
from typing import List, Any

import nextcord

from ...db_utils import fetch_one, fetch_all


async def get_server_autorole_state(guild_id: int) -> bool:
    autoroles_state = await fetch_one(
        f"SELECT autoroles_enabled FROM autoroles WHERE guild_id = {guild_id}"
    )[0]
    return bool(autoroles_state)


async def get_server_autorole_id(guild_id: int) -> int:
    autorole_id = await fetch_one(
        f"SELECT autorole_id FROM autoroles WHERE guild_id = {guild_id}"
    )[0]
    return autorole_id


async def get_server_reaction_autorole(
        guild_id: int, channel_id: int, message_id: int, reaction: str
) -> list[int]:
    list_of_autoroles = []
    async for row in await fetch_all(
            f"SELECT autorole_id FROM reaction_autorole WHERE guild_id = {guild_id} AND channel_id = {channel_id} AND "
            f"message_id = {message_id} AND reaction = '{reaction}'"
    ):
        list_of_autoroles.append(row[0])
    return list_of_autoroles


async def check_reaction_autorole(guild_id: int, role: nextcord.Role) -> bool:
    autorole_id = fetch_one(
        f"SELECT autorole_id FROM reaction_autorole WHERE guild_id = {guild_id} AND autorole_id = {role.id}"
    )
    if autorole_id is not None:
        return True
    else:
        return False


async def check_level_autorole(guild_id: int, level: int) -> bool:
    autorole_id = await fetch_one(
        f"SELECT autorole_id FROM autoroles_level WHERE guild_id = {guild_id} AND level = {level}"
    )
    if autorole_id is not None:
        return True
    else:
        return False


async def get_server_level_autorole(guild_id: int, level: int):
    autorole_id = await fetch_one(
        f"SELECT autorole_id FROM autoroles_level WHERE guild_id = {guild_id} AND level = {level}"
    )[0]
    return autorole_id


async def list_level_autoroles(guild_id: int):
    rows = await fetch_all(
        f"SELECT autorole_id, level FROM autoroles_level WHERE guild_id = {guild_id}"
    )
    return rows


async def list_reaction_autoroles(guild_id: int):
    rows = await fetch_all(
        f"SELECT autorole_id, reaction FROM reaction_autorole WHERE guild_id = {guild_id}"
    )
    return rows


async def get_autorole_lvl_deletion_state(guild_id: int) -> bool:
    remove_lvl_roles = await fetch_one(
        f"SELECT remove_lvl_roles FROM autorole_bool WHERE guild_id = {guild_id}"
    )
    return bool(remove_lvl_roles)


async def get_lesser_lvl_roles_list(guild_id: int, level: int) -> list:
    all_roles = await fetch_all(
        f"SELECT autorole_id FROM autoroles_level WHERE level < {level} AND guild_id = {guild_id}"
    )
    return all_roles


async def get_server_marriage_autorole(guild_id: int) -> int:
    marriage_autorole = await fetch_one(
        f"SELECT autorole_id FROM autoroles_marriage WHERE guild_id = {guild_id}"
    )
    return marriage_autorole
