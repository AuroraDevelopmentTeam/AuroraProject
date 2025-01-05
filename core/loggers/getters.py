from ..db_utils import fetch_one


async def get_logging_channel(guild_id: int) -> int:
    log_channel_id = await fetch_one(
        f"SELECT log_channel_id FROM loggers WHERE guild_id = {guild_id}"
    )
    return log_channel_id[0]


async def get_logging_state(guild_id: int) -> bool:
    logging_state = await fetch_one(
        f"SELECT logs_enabled FROM loggers WHERE guild_id = {guild_id}"
    )
    return bool(logging_state[0])
