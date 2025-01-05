from core.db_utils import execute_update


async def set_welcome_channel(guild_id: int, welcome_channel_id: int) -> None:
    sql = "UPDATE welcomers_config SET welcome_message_channel = %s WHERE guild_id = %s"
    values = (welcome_channel_id, guild_id)
    await execute_update(sql, values)


async def set_welcome_message_state(guild_id: int, welcome_message_enabled: bool) -> None:
    sql = "UPDATE welcomers_config SET welcome_message_enabled = %s WHERE guild_id = %s"
    values = (welcome_message_enabled, guild_id)
    await execute_update(sql, values)


async def update_welcome_message_type(guild_id: int, welcome_message_type: str) -> None:
    sql = "UPDATE welcomers_config SET welcome_message_type = %s WHERE guild_id = %s"
    values = (welcome_message_type, guild_id)
    await execute_update(sql, values)


async def update_welcome_message_title(guild_id: int, welcome_message_title: str) -> None:
    sql = "UPDATE welcomers_config SET welcome_message_title = %s WHERE guild_id = %s"
    values = (welcome_message_title, guild_id)
    await execute_update(sql, values)


async def update_welcome_message_description(
    guild_id: int, welcome_message_description: str
) -> None:
    sql = (
        "UPDATE welcomers_config SET welcome_message_description = %s WHERE guild_id = %s"
    )
    values = (welcome_message_description, guild_id)
    await execute_update(sql, values)


async def update_welcome_message_url(guild_id: int, welcome_message_url: str) -> None:
    sql = "UPDATE welcomers_config SET welcome_message_url = %s WHERE guild_id = %s"
    values = (welcome_message_url, guild_id)
    await execute_update(sql, values)
