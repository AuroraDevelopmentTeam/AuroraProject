import sqlite3
from ..db_utils import fetch_one

async def get_user_badge_state(guild_id: int, user_id: int, badge: str) -> bool:
    badge_state = await fetch_one(
        f"SELECT {badge} FROM badges WHERE guild_id = {guild_id} AND user_id = {user_id}"
    )
    return bool(badge_state[0])
