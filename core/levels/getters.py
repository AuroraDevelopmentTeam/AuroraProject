from ..db_utils import fetch_one


async def get_user_level(guild_id: int, user_id: int) -> int:
    level = await fetch_one(
        f"SELECT level FROM levels WHERE guild_id = {guild_id} AND user_id = {user_id}"
    )
    return level[0]


async def get_user_exp(guild_id: int, user_id: int) -> int:
    exp = await fetch_one(
        f"SELECT exp FROM levels WHERE guild_id = {guild_id} AND user_id = {user_id}"
    )
    return exp[0]


async def get_min_max_exp(guild_id: int) -> tuple[int, int]:
    min_exp = await fetch_one(
        f"SELECT min_exp_per_message FROM levels_config WHERE guild_id = {guild_id}"
    )
    max_exp = await fetch_one(
        f"SELECT max_exp_per_message FROM levels_config WHERE guild_id = {guild_id}"
    )
    return min_exp[0], max_exp[0]


async def get_guild_messages_state(guild_id: int) -> bool:
    messages_state = await fetch_one(
        f"SELECT level_up_messages_state FROM levels_config WHERE guild_id = {guild_id}"
    )
    return bool(messages_state[0])


async def get_channel_level_state(guild_id: int, channel_id: int) -> bool:
    state = await fetch_one(
        f"SELECT enabled FROM level_channels_config WHERE guild_id = {guild_id} AND channel_id = {channel_id}"
    )
    if state is None:
        return True
    else:
        state = state[0]
        return bool(state)
