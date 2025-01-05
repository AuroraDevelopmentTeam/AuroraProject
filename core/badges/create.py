import sqlite3
from ..db_utils import execute_update


async def create_badges_table() -> None:
    await execute_update(
        f"""CREATE TABLE IF NOT EXISTS badges (
        guild_id BIGINT, user_id BIGINT, badge_1 BOOL, badge_2 BOOL, badge_3 BOOL, badge_4 BOOL, 
        badge_5 BOOL, badge_6 BOOL, badge_7 BOOL, badge_8 BOOL, badge_9 BOOL
    )"""
    )
