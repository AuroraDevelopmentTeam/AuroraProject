import sqlite3

from ..db_utils import execute_update

async def update_min_bet(guild_id: int, min_bet: int) -> None:
    sql = "UPDATE bets SET min_bet = %s WHERE guild_id = %s"
    values = (min_bet, guild_id)
    await execute_update(sql, values)


async def update_max_bet(guild_id: int, max_bet: int) -> None:
    sql = "UPDATE bets SET max_bet = %s WHERE guild_id = %s"
    values = (max_bet, guild_id)
    await execute_update(sql, values)
