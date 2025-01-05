import sqlite3

from ..db_utils import execute_update

async def update_emotions_for_money_state(guild_id: int, state: bool) -> None:
    sql = "UPDATE emotions_cost SET emotions_for_money_state = %s WHERE guild_id = %s"
    values = (state, guild_id)
    await execute_update(sql, values)


async def update_emotions_cost(guild_id: int, cost: int) -> None:
    sql = "UPDATE emotions_cost SET cost = %s WHERE guild_id = %s"
    values = (cost, guild_id)
    await execute_update(sql, values)