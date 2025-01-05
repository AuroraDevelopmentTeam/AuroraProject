from core.db_utils import execute_update


async def update_voice_creation_room(guild_id: int, voice_creation_room_id: int) -> None:
    sql = "UPDATE voice_private_config SET voice_creation_room_id = ? WHERE guild_id = ?"
    values = (voice_creation_room_id, guild_id)
    await execute_update(sql, values)


async def update_voice_controller_msg(guild_id: int, voice_controller_msg_id: int) -> None:
    sql = "UPDATE voice_private_config SET voice_controller_msg_id = ? WHERE guild_id = ?"
    values = (voice_controller_msg_id, guild_id)
    await execute_update(sql, values)
