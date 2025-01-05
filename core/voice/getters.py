from core.db_utils import fetch_one


async def get_voice_creation_room(guild_id: int) -> int:
    voice_creation_room = await fetch_one(
        f"SELECT voice_creation_room_id FROM voice_private_config WHERE guild_id = {guild_id}"
    )
    return voice_creation_room[0]


async def get_voice_controller_msg(guild_id: int) -> int:
    voice_controller_msg = await fetch_one(
        f"SELECT voice_controller_msg_id FROM voice_private_config WHERE guild_id = {guild_id}"
    )
    return voice_controller_msg[0]
