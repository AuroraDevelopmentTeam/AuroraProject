import sqlite3
from core.checkers import is_guild_id_in_table, is_user_in_table

from ..db_utils import execute_update

async def write_in_emotions_cost_standart_values(guilds) -> None:
    for guild in guilds:
        if await is_guild_id_in_table("emotions_cost", guild.id) is False:
            sql = (
                "INSERT INTO emotions_cost(guild_id, emotions_for_money_state, cost) VALUES (%s, %s, %s)"
            )
            val = (
                guild.id,
                False,
                0
            )
            await execute_update(sql, val)
