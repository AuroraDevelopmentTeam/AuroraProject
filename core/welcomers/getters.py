from core.db_utils import fetch_one


async def get_server_welcome_channel_id(guild_id: int) -> int:
    welcome_channel_id = await fetch_one(
        f"SELECT welcome_message_channel FROM welcomers_config WHERE guild_id = {guild_id}"
    )
    return welcome_channel_id[0]


async def get_server_welcome_state(guild_id: int) -> bool:
    messages_state = await fetch_one(
        f"SELECT welcome_message_enabled FROM welcomers_config WHERE guild_id = {guild_id}"
    )
    return bool(messages_state[0])


async def get_server_welcome_message_type(guild_id: int) -> str:
    messages_type = await fetch_one(
        f"SELECT welcome_message_type FROM welcomers_config WHERE guild_id = {guild_id}"
    )
    return messages_type[0]
