from ..db_utils import execute_update


async def create_loggers_table() -> None:
    await execute_update(
        f"""CREATE TABLE IF NOT EXISTS loggers (
        guild_id BIGINT, log_channel_id BIGINT, logs_enabled BOOL
    )"""
    )
