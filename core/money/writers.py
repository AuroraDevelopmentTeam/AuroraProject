import sqlite3
from core.checkers import is_guild_id_in_table, is_user_in_table
import json
from config import settings


def write_in_money_config_standart_values(guilds) -> None:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    for guild in guilds:
        if is_guild_id_in_table("money_config", guild.id) is False:
            sql = "INSERT INTO money_config(guild_id, guild_currency, guild_payday_time, guild_payday_amount, " \
                  "guild_starting_balance) VALUES (?, ?, ?, ?, ?)"
            val = (guild.id, settings['default_currency'], settings['default_payday_time'],
                   settings['default_payday_amount'], settings['default_starting_balance'])
            cursor.execute(sql, val)
            db.commit()
    cursor.close()
    db.close()
    return


def write_in_money_standart_values(guilds) -> None:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    for guild in guilds:
        guild_starting_balance = \
            cursor.execute(f"SELECT guild_starting_balance FROM money_config WHERE guild_id = {guild.id}").fetchone()[0]
        for member in guild.members:
            if not member.bot:
                if is_user_in_table("money", guild.id, member.id) is False:
                    sql = "INSERT INTO money(guild_id, user_id, balance) VALUES (?, ?, ?)"
                    val = (guild.id, member.id, guild_starting_balance)
                    cursor.execute(sql, val)
                    db.commit()
    cursor.close()
    db.close()
    return