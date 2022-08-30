import sqlite3

from core.clan.getters import get_user_clan_id, get_clan_owner_id


def is_user_in_clan(guild_id: int, user_id: int) -> bool:
    user_clan_id = get_user_clan_id(guild_id, user_id)
    if user_clan_id == 0:
        return False
    else:
        return True


def is_clan_owner(guild_id: int, user_id: int) -> bool:
    clan_owner_id = get_clan_owner_id(guild_id, user_id)
    if user_id == clan_owner_id:
        return True
    else:
        return False
