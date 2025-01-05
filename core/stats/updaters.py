from core.stats.getters import get_user_time_in_voice, get_user_messages_counter
from core.db_utils import execute_update


async def update_user_messages_counter(
    guild_id: int, user_id: int, messages_to_add: int
) -> None:
    messages_counter = await get_user_messages_counter(guild_id, user_id)
    sql = "UPDATE stats SET messages = %s WHERE guild_id = %s AND user_id = %s"
    values = (messages_counter + messages_to_add, guild_id, user_id)
    await execute_update(sql, values)


async def update_user_time_in_voice(guild_id: int, user_id: int, time_to_add: int) -> None:
    voice_time = get_user_time_in_voice(guild_id, user_id)
    sql = "UPDATE stats SET in_voice = %s WHERE guild_id = %s AND user_id = %s"
    values = (voice_time + time_to_add, guild_id, user_id)
    await execute_update(sql, values)


async def update_user_join_time(guild_id: int, user_id: int, join_time: str) -> None:
    sql = "UPDATE stats SET join_time = %s WHERE guild_id = %s AND user_id = %s"
    values = (join_time, guild_id, user_id)
    await execute_update(sql, values)
