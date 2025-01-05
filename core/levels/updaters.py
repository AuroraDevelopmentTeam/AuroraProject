import random
from ..db_utils import execute_update

from core.levels.getters import get_user_exp, get_user_level


async def update_user_exp(guild_id: int, user_id: int, min_exp: int, max_exp: int) -> None:
    if min_exp == max_exp:
        exp_to_add = min_exp
    else:
        exp_to_add = random.randint(min_exp, max_exp)
    exp_now = await get_user_exp(guild_id, user_id)
    sql = "UPDATE levels SET exp = %s WHERE guild_id = %s AND user_id = %s"
    values = (exp_now + exp_to_add, guild_id, user_id)
    await execute_update(sql, values)


async def update_user_level(guild_id: int, user_id: int, levels_to_add: int) -> None:
    level_now = await get_user_level(guild_id, user_id)
    sql = "UPDATE levels SET level = %s WHERE guild_id = %s AND user_id = %s"
    values = (level_now + levels_to_add, guild_id, user_id)
    await execute_update(sql, values)


async def set_user_level(guild_id: int, user_id: int, level: int) -> None:
    sql = "UPDATE levels SET level = %s WHERE guild_id = %s AND user_id = %s"
    values = (level, guild_id, user_id)
    await execute_update(sql, values)


async def set_user_exp_to_zero(guild_id: int, user_id: int) -> None:
    sql = "UPDATE levels SET exp = %s WHERE guild_id = %s AND user_id = %s"
    values = (0, guild_id, user_id)
    await execute_update(sql, values)


async def set_server_level_up_messages_state(guild_id: int, messages_state: bool) -> None:
    sql = "UPDATE levels_config SET level_up_messages_state = %s WHERE guild_id = %s"
    values = (messages_state, guild_id)
    await execute_update(sql, values)


async def update_min_max_exp(guild_id: int, min: int, max: int) -> None:
    sql = "UPDATE levels_config SET min_exp_per_message = %s WHERE guild_id = %s"
    values = (min, guild_id)
    await execute_update(sql, values)
    sql = "UPDATE levels_config SET max_exp_per_message = %s WHERE guild_id = %s"
    values = (max, guild_id)
    await execute_update(sql, values)
