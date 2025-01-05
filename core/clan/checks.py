import sqlite3

from core.clan.getters import (
    get_user_clan_id,
    get_clan_owner_id,
    get_clan_guild_boss_hp,
)

from ..db_utils import fetch_one

async def is_user_in_clan(guild_id: int, user_id: int) -> bool:
    user_clan_id = await get_user_clan_id(guild_id, user_id)
    if user_clan_id == 0:
        return False
    else:
        return True


async def is_clan_owner(guild_id: int, user_id: int) -> bool:
    clan_id = await get_user_clan_id(guild_id, user_id)
    clan_owner_id = await get_clan_owner_id(guild_id, clan_id)
    if user_id == clan_owner_id:
        return True
    else:
        return False


async def is_clan_id_in_table(guild_id: int, clan_id: int) -> bool:
    clan_id = await fetch_one(
        f"SELECT clan_id FROM clans WHERE guild_id = {guild_id} AND clan_id = {clan_id}"
    )
    if clan_id is None:
        return False
    else:
        return True


async def boss_alive(guild_id: int, clan_id: int) -> bool:
    hp = await get_clan_guild_boss_hp(guild_id, clan_id)
    return True if hp > 0 else False
