import sqlite3

from core.money.getters import get_user_balance
from ..db_utils import execute_update

async def update_guild_currency_symbol(guild_id: int, currency_symbol: str) -> None:
    sql = "UPDATE money_config SET guild_currency = %s WHERE guild_id = %s"
    values = (currency_symbol, guild_id)
    await execute_update(sql, values)


async def update_guild_starting_balance(guild_id: int, balance: int) -> None:
    sql = "UPDATE money_config SET guild_starting_balance = %s WHERE guild_id = %s"
    values = (balance, guild_id)
    await execute_update(sql, values)


async def update_guild_payday_amount(guild_id: int, payday_amount: int) -> None:
    sql = "UPDATE money_config SET guild_payday_amount = %s WHERE guild_id = %s"
    values = (payday_amount, guild_id)
    await execute_update(sql, values)


async def update_user_balance(guild_id: int, user_id: int, money: int) -> None:
    balance = await get_user_balance(guild_id, user_id)
    sql = "UPDATE money SET balance = %s WHERE guild_id = %s AND user_id = %s"
    values = (balance + money, guild_id, user_id)
    await execute_update(sql, values)


async def set_user_balance(guild_id: int, user_id: int, money: int) -> None:
    sql = "UPDATE money SET balance = %s WHERE guild_id = %s AND user_id = %s"
    values = (money, guild_id, user_id)
    await execute_update(sql, values)


async def update_guild_min_max_msg_income(
    guild_id: int, min_income: int, max_income: int
) -> None:
    sql = "UPDATE chat_money_config SET min_msg_income = %s WHERE guild_id = %s"
    values = (min_income, guild_id)
    await execute_update(sql, values)
    sql = "UPDATE chat_money_config SET max_msg_income = %s WHERE guild_id =%s?"
    values = (max_income, guild_id)
    await execute_update(sql, values)


async def update_guild_min_max_voice_income(
    guild_id: int, min_income: int, max_income: int
) -> None:
    sql = "UPDATE chat_money_config SET min_voice_income = ? WHERE guild_id = ?"
    values = (min_income, guild_id)
    await execute_update(sql, values)
    sql = "UPDATE chat_money_config SET max_voice_income = ? WHERE guild_id = ?"
    values = (max_income, guild_id)
    await execute_update(sql, values)


async def update_guild_msg_cooldown(guild_id: int, msg_per_income: int) -> None:
    sql = "UPDATE chat_money_config SET msg_cooldown = ? WHERE guild_id = ?"
    values = (msg_per_income, guild_id)
    await execute_update(sql, values)



async def update_guild_voice_minutes_for_money(guild_id: int, voice_minutes: int) -> None:
    sql = "UPDATE chat_money_config SET voice_minutes_for_money = ? WHERE guild_id = ?"
    values = (voice_minutes, guild_id)
    await execute_update(sql, values)
