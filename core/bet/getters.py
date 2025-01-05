import sqlite3

from ..db_utils import fetch_one

async def get_min_bet(guild_id: int) -> int:
    min_bet = await fetch_one(
        f"SELECT min_bet FROM bets WHERE guild_id = {guild_id}"
    )
    return min_bet[0]


async def get_max_bet(guild_id: int) -> int:
    max_bet = await fetch_one(
        f"SELECT max_bet FROM bets WHERE guild_id = {guild_id}"
    )
    return max_bet[0]
