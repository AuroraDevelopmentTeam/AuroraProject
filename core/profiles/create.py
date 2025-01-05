from core.db_utils import execute_update


async def create_profiles_table() -> None:
    await execute_update(
        f"""CREATE TABLE IF NOT EXISTS profiles (
        user_id BIGINT, description TEXT, avatar_form TEXT
    )"""
    )
