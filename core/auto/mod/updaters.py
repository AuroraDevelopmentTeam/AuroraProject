from ...db_utils import execute_update

async def update_server_word_detect(guild_id: int, word_detect_state: bool) -> None:
    sql = "UPDATE mod_config SET word_detect = %s WHERE guild_id = %s"
    values = (word_detect_state, guild_id)
    await execute_update(sql, values)


async def update_server_link_detect(guild_id: int, link_detect_state: bool) -> None:
    sql = "UPDATE mod_config SET link_detect = %s WHERE guild_id = %s"
    values = (link_detect_state, guild_id)
    await execute_update(sql, values)


async def update_server_nickname_detect(guild_id: int, nickname_detect_state: bool) -> None:
    sql = "UPDATE mod_config SET nickname_detect = %s WHERE guild_id = %s"
    values = (nickname_detect_state, guild_id)
    await execute_update(sql, values)


async def update_server_status_detect(guild_id: int, status_detect_state: bool) -> None:
    sql = "UPDATE mod_config SET status_detect = %s WHERE guild_id = %s"
    values = (status_detect_state, guild_id)
    await execute_update(sql, values)


async def update_server_moderation_mode(guild_id: int, moderation_mode: str) -> None:
    sql = "UPDATE mod_config SET guild_moderation_mode = %s WHERE guild_id = %s"
    values = (moderation_mode, guild_id)
    await execute_update(sql, values)
