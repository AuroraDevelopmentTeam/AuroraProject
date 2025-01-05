import sqlite3
import nextcord
from core.checkers import is_guild_id_in_table, is_user_in_table
import json
from config import settings
from core.money.getters import get_channel_income_state
from ..db_utils import execute_update, fetch_one


async def write_in_money_config_standart_values(guilds) -> None:
    for guild in guilds:
        if await is_guild_id_in_table("money_config", guild.id) is False:
            sql = (
                "INSERT INTO money_config(guild_id, guild_currency, guild_payday_amount, "
                "guild_starting_balance) VALUES (%s, %s, %s, %s)"
            )
            val = (
                guild.id,
                settings["default_currency"],
                settings["default_payday_amount"],
                settings["default_starting_balance"],
            )
            await execute_update(sql, val)


async def write_in_money_standart_values(guilds: list) -> None:
    for guild in guilds:
        guild_starting_balance = await fetch_one(
            f"SELECT guild_starting_balance FROM money_config WHERE guild_id = {guild.id}"
        )
        for member in guild.members:
            if not member.bot:
                if await is_user_in_table("money", guild.id, member.id) is False:
                    sql = (
                        "INSERT INTO money(guild_id, user_id, balance) VALUES (%s, %s, %s)"
                    )
                    val = (guild.id, member.id, guild_starting_balance[0])
                    await execute_update(sql, val)


async def write_role_in_income(guild_id: int, role: nextcord.Role, income: int) -> None:
    sql = "INSERT INTO roles_money(guild_id, role_id, income) VALUES (%s, %s, %s)"
    val = (guild_id, role.id, income)
    await execute_update(sql, val)


async def delete_role_from_income(guild_id: int, role: nextcord.Role) -> None:
    sql = f"DELETE FROM roles_money WHERE role_id = {role.id} AND guild_id = {guild_id}"
    await execute_update(sql)


async def write_channel_in_config(guild_id: int, channel_id: int, enabled: bool) -> None:
    if enabled is True:
        if await get_channel_income_state(guild_id, channel_id) is False:
            try:
                sql = f"DELETE FROM money_channels_config WHERE guild_id = {guild_id} AND channel_id = {channel_id}"
                await execute_update(sql)
            except:
                pass
    else:
        sql = "INSERT INTO money_channels_config(guild_id, channel_id, enabled) VALUES (%s, %s, %s)"
        val = (guild_id, channel_id, enabled)
        await execute_update(sql, val)


async def write_in_chat_money_standart_values(guilds) -> None:
    for guild in guilds:
        if await is_guild_id_in_table("chat_money_config", guild.id) is False:
            sql = (
                "INSERT INTO chat_money_config(guild_id, min_msg_income, max_msg_income, "
                "msg_cooldown, min_voice_income, max_voice_income, voice_minutes_for_money) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s)"
            )
            val = (guild.id, 0, 1, 5, 1, 2, 2)
            await execute_update(sql, val)
