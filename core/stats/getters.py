from core.db_utils import fetch_one


async def get_user_messages_counter(guild_id: int, user_id: int) -> int:
    messages_counter = await fetch_one(
        f"SELECT messages FROM stats WHERE guild_id = {guild_id} AND user_id = {user_id}"
    )
    return messages_counter[0]


async def get_user_time_in_voice(guild_id: int, user_id: int) -> int:
    in_voice = await fetch_one(
        f"SELECT in_voice FROM stats WHERE guild_id = {guild_id} AND user_id = {user_id}"
    )
    return in_voice[0]


async def get_user_join_time(guild_id: int, user_id: int) -> str:
    join_time = await fetch_one(
        f"SELECT join_time FROM stats WHERE guild_id = {guild_id} AND user_id = {user_id}"
    )
    return join_time[0]


async def get_channel_stats_state(guild_id: int, channel_id: int) -> bool:
    state = await fetch_one(
        f"SELECT enabled FROM stats_channels_config WHERE guild_id = {guild_id} AND channel_id = {channel_id}"
    )
    if state is None:
        return True
    else:
        state = state[0]
        return bool(state)
