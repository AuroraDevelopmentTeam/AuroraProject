import sqlite3
from core.checkers import is_guild_id_in_table, is_user_in_table

from ..db_utils import execute_update

async def write_in_bets_standart_values(guilds) -> None:
    for guild in guilds:
        if await is_guild_id_in_table("bets", guild.id) is False:
            sql = (
                "INSERT INTO bets(guild_id, min_bet, max_bet) VALUES (%s, %s, %s)"
            )
            val = (
                guild.id,
                1,
                1000000
            )
            await execute_update(sql, val)