from ..db_utils import fetch_one


async def get_server_nitro_channel_id(guild_id: int) -> int:
    nitro_channel_id = await fetch_one(
        f"SELECT nitro_message_channel FROM on_nitro_config WHERE guild_id = {guild_id}"
    )
    return nitro_channel_id[0]


async def get_server_nitro_state(guild_id: int) -> bool:
    messages_state = await fetch_one(
        f"SELECT nitro_message_enabled FROM on_nitro_config WHERE guild_id = {guild_id}"
    )
    return bool(messages_state[0])
