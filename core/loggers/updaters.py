from ..db_utils import execute_update


async def update_logging_channel_id(guild_id: int, logging_channel_id: int) -> None:
    sql = "UPDATE loggers SET log_channel_id = %s WHERE guild_id = %s"
    values = (logging_channel_id, guild_id)
    await execute_update(sql, values)


async def update_logging_guild_state(guild_id: int, logging_state: bool) -> None:
    sql = "UPDATE loggers SET logs_enabled = %s WHERE guild_id = %s"
    values = (logging_state, guild_id)
    await execute_update(sql, values)
