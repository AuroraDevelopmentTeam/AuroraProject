from ..db_utils import fetch_one


async def get_server_goodbye_channel_id(guild_id: int) -> int:
    goodbye_channel_id = await fetch_one(
        f"SELECT goodbye_message_channel FROM goodbye_config WHERE guild_id = {guild_id}"
    )
    return goodbye_channel_id[0]


async def get_server_goodbye_state(guild_id: int) -> bool:
    messages_state = await fetch_one(
        f"SELECT goodbye_message_enabled FROM goodbye_config WHERE guild_id = {guild_id}"
    )
    return bool(messages_state[0])


async def get_server_goodbye_message_type(guild_id: int) -> str:
    messages_type = await fetch_one(
        f"SELECT goodbye_message_type FROM goodbye_config WHERE guild_id = {guild_id}"
    )
    return messages_type[0]
