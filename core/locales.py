import sqlite3
from core.checkers import is_guild_id_in_table
import json


def create_locales_table() -> None:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    cursor.execute(f"""CREATE TABLE IF NOT EXISTS locales (
        guild_id, locale TEXT
    )""")
    db.commit()
    cursor.close()
    db.close()
    return


def write_in_locales_standart_values(guilds) -> None:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    for guild in guilds:
        if is_guild_id_in_table("locales", guild.id) is False:
            sql = "INSERT INTO locales(guild_id, locale) VALUES (?, ?)"
            val = (guild.id, 'en_us')
            cursor.execute(sql, val)
            db.commit()
    cursor.close()
    db.close()


def get_guild_locale(guild_id: int) -> str:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    locale = cursor.execute(f"SELECT locale FROM locales WHERE guild_id = {guild_id}").fetchone()[0]
    cursor.close()
    db.close()
    return locale


def update_guild_locale(locale, guild_id) -> None:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    sql = "UPDATE locales SET locale = ? WHERE guild_id = ?"
    values = (locale, guild_id)
    cursor.execute(sql, values)
    db.commit()
    cursor.close()
    db.close()
    return


def get_msg_from_locale_by_key(guild_id: int, key: str) -> str:
    locale = get_guild_locale(guild_id)

    with open(f'./locales/{locale}.json', 'r', encoding='utf-8') as file:
        locales_file = json.load(file)

    return locales_file[key]['msg']


def get_keys_in_locale(guild_id: int, command_name: str) -> list:
    locale = get_guild_locale(guild_id)

    keys_list = []

    with open(f'./locales/{locale}.json', 'r', encoding='utf-8') as file:
        locales_file = json.load(file)

    for key in locales_file[command_name]:
        keys_list.append(key)

    return keys_list


def get_keys_value_in_locale(guild_id: int, command_name: str) -> list:
    keys = get_keys_in_locale(guild_id, command_name)
    keys_value = []
    locale = get_guild_locale(guild_id)
    with open(f'./locales/{locale}.json', 'r', encoding='utf-8') as file:
        locales_file = json.load(file)

    for key in keys:
        keys_value.append(locales_file[command_name][key])

    return keys_value
