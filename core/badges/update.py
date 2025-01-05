import sqlite3
from ..db_utils import execute_update

async def update_user_badge_state(
    guild_id: int, user_id: int, badge: str, state: bool
) -> None:
    sql = f"UPDATE badges SET {badge} = %s WHERE guild_id = %s AND user_id = %s"
    values = (state, guild_id, user_id)
    await execute_update(sql, values)
