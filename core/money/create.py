import sqlite3
from core.checkers import is_guild_id_in_table, is_user_in_table
import json


def create_money_table() -> None:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    cursor.execute(f"""CREATE TABLE IF NOT EXISTS money (
        guild_id INTERGER, user_id INTERGER, balance INTERGER
    )""")
    db.commit()
    cursor.close()
    db.close()
    return


def create_money_config_table() -> None:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    cursor.execute(f"""CREATE TABLE IF NOT EXISTS money_config (
        guild_id INTERGER, guild_currency TEXT, guild_payday_time INTERGER, guild_payday_amount INTERGER, 
        guild_starting_balance INTERGER
    )""")
    db.commit()
    cursor.close()
    db.close()
    return