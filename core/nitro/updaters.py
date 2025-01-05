from core.db_utils import execute_update


async def set_nitro_channel(guild_id: int, nitro_channel_id: int) -> None:
    sql = "UPDATE on_nitro_config SET nitro_message_channel = %s WHERE guild_id = %s"
    values = (nitro_channel_id, guild_id)
    await execute_update(sql, values)


async def set_nitro_message_state(guild_id: int, nitro_message_enabled: bool) -> None:
    sql = "UPDATE on_nitro_config SET nitro_message_enabled = %s WHERE guild_id = %s"
    values = (nitro_message_enabled, guild_id)
    await execute_update(sql, values)


async def update_nitro_message_title(guild_id: int, nitro_message_title: str) -> None:
    sql = "UPDATE on_nitro_config SET nitro_message_title = %s WHERE guild_id = %s"
    values = (nitro_message_title, guild_id)
    await execute_update(sql, values)


async def update_nitro_message_description(
    guild_id: int, nitro_message_description: str
) -> None:
    sql = "UPDATE on_nitro_config SET nitro_message_description = %s WHERE guild_id = %s"
    values = (nitro_message_description, guild_id)
    await execute_update(sql, values)


async def update_nitro_message_url(guild_id: int, nitro_message_url: str) -> None:
    sql = "UPDATE on_nitro_config SET nitro_message_url = %s WHERE guild_id = %s"
    values = (nitro_message_url, guild_id)
    await execute_update(sql, values)
