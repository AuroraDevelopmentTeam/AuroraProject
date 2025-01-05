from ..db_utils import execute_update


async def create_honor_table() -> None:
    await execute_update(
        f"""CREATE TABLE IF NOT EXISTS honor (
        user_id BIGINT, honor_level INTEGER, honor_points INTEGER
    )"""
    )
