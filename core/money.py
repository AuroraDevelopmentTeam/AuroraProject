import sqlite3
from core.checkers import is_guild_id_in_table, is_user_in_table
import json
from config import settings


def create_money_table() -> None:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    cursor.execute(f"""CREATE TABLE IF NOT EXISTS money (
        guild_id INTERGER, user_id INTERGER balance INTERGER
    )""")
    db.commit()
    cursor.close()
    db.close()
    return


def create_money_config_table() -> None:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    cursor.execute(f"""CREATE TABLE IF NOT EXISTS money_config (
        guild_id INTERGER, guild_currency TEXT, guild_payday_time INTERGER, guild_payday_amount INTERGER
    )""")
    db.commit()
    cursor.close()
    db.close()
    return


def write_in_money_config_standart_values(guilds) -> None:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    for guild in guilds:
        if is_guild_id_in_table("money_config", guild.id) is False:
            sql = "INSERT INTO money_config(guild_id, guild_currency, guild_payday_time, guild_payday_amount) " \
                  "VALUES (?, ?, ?, ?)"
            val = (guild.id, settings['default_currency'], settings['default_payday_time'],
                   settings['default_payday_amount'])
            cursor.execute(sql, val)
            db.commit()
    cursor.close()
    db.close()
    return


def write_in_money_standart_values(guilds) -> None:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    for guild in guilds:
        for member in guild.members:
            if not member.bot:
                if is_user_in_table("money", guild.id, member.id) is False:
                    sql = "INSERT INTO money(guild_id, user_id, balance) VALUES (?, ?, ?)"
                    val = (guild.id, member.id, settings['default_starting_balance'])
                    cursor.execute(sql, val)
                    db.commit()
    cursor.close()
    db.close()
    return
