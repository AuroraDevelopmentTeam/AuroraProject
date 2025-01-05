from core.db_utils import execute_update


async def create_warns_table() -> None:
    await execute_update(
        f"""CREATE TABLE IF NOT EXISTS warns (
        warn_id INTEGER, guild_id BIGINT, user_id BIGINT, warn_reason TEXT
    )"""
    )
