import sqlite3
import nextcord
from core.checkers import is_guild_id_in_table, is_user_in_table
import json
from config import settings
from core.money.getters import get_channel_income_state


def write_in_money_config_standart_values(guilds) -> None:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    for guild in guilds:
        if is_guild_id_in_table("money_config", guild.id) is False:
            sql = (
                "INSERT INTO money_config(guild_id, guild_currency, guild_payday_amount, "
                "guild_starting_balance) VALUES (?, ?, ?, ?)"
            )
            val = (
                guild.id,
                settings["default_currency"],
                settings["default_payday_amount"],
                settings["default_starting_balance"],
            )
            cursor.execute(sql, val)
            db.commit()
    cursor.close()
    db.close()
    return


def write_in_money_standart_values(guilds: list) -> None:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    for guild in guilds:
        guild_starting_balance = cursor.execute(
            f"SELECT guild_starting_balance FROM money_config WHERE guild_id = {guild.id}"
        ).fetchone()[0]
        for member in guild.members:
            if not member.bot:
                if is_user_in_table("money", guild.id, member.id) is False:
                    sql = (
                        "INSERT INTO money(guild_id, user_id, balance) VALUES (?, ?, ?)"
                    )
                    val = (guild.id, member.id, guild_starting_balance)
                    cursor.execute(sql, val)
                    db.commit()
    cursor.close()
    db.close()
    return


def write_role_in_income(guild_id: int, role: nextcord.Role, income: int) -> None:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    sql = "INSERT INTO roles_money(guild_id, role_id, income) VALUES (?, ?, ?)"
    val = (guild_id, role.id, income)
    cursor.execute(sql, val)
    db.commit()
    cursor.close()
    db.close()


def delete_role_from_income(guild_id: int, role: nextcord.Role) -> None:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    sql = f"DELETE FROM roles_money WHERE role_id = {role.id} AND guild_id = {guild_id}"
    cursor.execute(sql)
    db.commit()
    cursor.close()
    db.close()


def write_channel_in_config(guild_id: int, channel_id: int, enabled: bool) -> None:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    if enabled is True:
        if get_channel_income_state(guild_id, channel_id) is False:
            try:
                sql = f"DELETE FROM money_channels_config WHERE guild_id = {guild_id} AND channel_id = {channel_id}"
                cursor.execute(sql)
                db.commit()
            except:
                pass
        else:
            pass
    else:
        sql = "INSERT INTO money_channels_config(guild_id, channel_id, enabled) VALUES (?, ?, ?)"
        val = (guild_id, channel_id, enabled)
        cursor.execute(sql, val)
    db.commit()
    cursor.close()
    db.close()


def write_in_chat_money_standart_values(guilds) -> None:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    for guild in guilds:
        if is_guild_id_in_table("chat_money_config", guild.id) is False:
            sql = (
                "INSERT INTO chat_money_config(guild_id, min_msg_income, max_msg_income, "
                "msg_cooldown, min_voice_income, max_voice_income, voice_minutes_for_money) "
                "VALUES (?, ?, ?, ?, ?, ?, ?)"
            )
            val = (guild.id, 0, 1, 5, 1, 2, 2)
            cursor.execute(sql, val)
            db.commit()
    cursor.close()
    db.close()
    return
