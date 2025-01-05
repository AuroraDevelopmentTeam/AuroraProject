from core.db_utils import execute_update


async def create_stats_table() -> None:
    await execute_update(
        f"""CREATE TABLE IF NOT EXISTS stats (    guild_id BIGINT,     user_id BIGINT,     messages INTEGER,     in_voice INTEGER,     join_time TEXT)"""
    )


async def create_stats_channels_config_table() -> None:
    await execute_update(
        f"""CREATE TABLE IF NOT EXISTS stats_channels_config (
        guild_id BIGINT, channel_id BIGINT, enabled BOOL)"""
    )
