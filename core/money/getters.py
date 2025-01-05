import sqlite3
from typing import Any

from ..db_utils import fetch_all, fetch_one


async def get_user_balance(guild_id: int, user_id: int) -> int:
    balance = await fetch_one(
        f"SELECT balance FROM money WHERE guild_id = {guild_id} AND user_id = {user_id}"
    )
    return balance[0]


async def get_guild_currency_symbol(guild_id: int) -> str:
    currency_symbol = await fetch_one(
        f"SELECT guild_currency FROM money_config" f" WHERE guild_id = {guild_id}"
    )
    return currency_symbol[0]


async def get_guild_starting_balance(guild_id: int) -> int:
    starting_balance = await fetch_one(
        f"SELECT guild_starting_balance FROM money_config"
        f" WHERE guild_id = {guild_id}"
    )
    return starting_balance[0]


async def get_guild_payday_amount(guild_id: int) -> int:
    payday_amount = await fetch_one(
        f"SELECT guild_payday_amount FROM money_config" f" WHERE guild_id = {guild_id}"
    )
    return payday_amount[0]


async def get_guild_min_max_msg_income(guild_id: int) -> list[tuple | Any]:
    income = await fetch_one(
        f"SELECT min_msg_income, max_msg_income FROM chat_money_config"
        f" WHERE guild_id = {guild_id}"
    )
    min_income = income[0]
    max_income = income[1]
    return [min_income, max_income]


async def get_msg_cooldown(guild_id: int) -> int:
    msg_cooldown = await fetch_one(
        f"SELECT msg_cooldown FROM chat_money_config" f" WHERE guild_id = {guild_id}"
    )
    return msg_cooldown[0]


async def get_guild_min_max_voice_income(guild_id: int) -> list[tuple | Any]:
    income = await fetch_one(
        f"SELECT min_voice_income, max_voice_income FROM chat_money_config"
        f" WHERE guild_id = {guild_id}"
    )
    min_income = income[0]
    max_income = income[1]
    return [min_income, max_income]


async def get_voice_minutes_for_income(guild_id: int) -> int:
    voice_minutes = await fetch_one(
        f"SELECT voice_minutes_for_money FROM chat_money_config"
        f" WHERE guild_id = {guild_id}"
    )
    return voice_minutes[0]


async def get_channel_income_state(guild_id: int, channel_id: int) -> bool:
    messages_state = await fetch_one(
        f"SELECT enabled FROM money_channels_config WHERE guild_id = {guild_id} AND channel_id = {channel_id}"
    )
    if messages_state is None:
        return True
    else:
        state = messages_state[0]
        return bool(state)


async def list_income_roles(guild_id: int):
    rows = await fetch_all(
        f"SELECT role_id, income FROM roles_money WHERE guild_id = {guild_id}"
    )
    return rows


async def get_all_users(guild_id: int) -> list[tuple[int]]:
    rows = await fetch_all(
        f"SELECT user_id FROM money WHERE guild_id = {guild_id}"
    )
    rows_list = []
    for row in rows:
        rows_list.append(row[0])
    return rows_list
