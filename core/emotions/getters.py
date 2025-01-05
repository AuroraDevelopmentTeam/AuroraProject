import sqlite3

from ..db_utils import fetch_one

async def get_emotions_for_money_state(guild_id: int) -> bool:
    emotions_for_money_state = await fetch_one(
        f"SELECT emotions_for_money_state FROM emotions_cost WHERE guild_id = {guild_id}"
    )[0]
    return bool(emotions_for_money_state)


async def get_emotions_cost(guild_id: int) -> int:
    emotions_cost = await fetch_one(
        f"SELECT cost FROM emotions_cost WHERE guild_id = {guild_id}"
    )[0]
    return emotions_cost


async def is_emotion_free(guild_id: int) -> bool:
    emotions_for_money_state = await get_emotions_for_money_state(guild_id)
    if emotions_for_money_state is False:
        return True
    else:
        emotions_cost = await get_emotions_cost(guild_id)
        if emotions_cost == 0:
            return True
        else:
            return False

