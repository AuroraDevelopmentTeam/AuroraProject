import sqlite3
from core.checkers import is_guild_id_in_table
import json
from config import settings

LOCALE_LIST = ["ru_ru", "en_us"]


def get_guild_locale(guild_id: int) -> str:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    locale = cursor.execute(
        f"SELECT locale FROM locales WHERE guild_id = {guild_id}"
    ).fetchone()[0]
    cursor.close()
    db.close()
    return locale


def get_msg_from_locale_by_key(guild_id: int, key: str) -> str:
    locale = get_guild_locale(guild_id)

    with open(f"./locales/{locale}.json", "r", encoding="utf-8") as file:
        locales_file = json.load(file)

    return locales_file[key]["msg"]


def get_keys_in_locale(guild_id: int, command_name: str) -> list:
    locale = get_guild_locale(guild_id)

    keys_list = []

    with open(f"./locales/{locale}.json", "r", encoding="utf-8") as file:
        locales_file = json.load(file)

    for key in locales_file[command_name]:
        if key != "name" and key != "description":
            keys_list.append(key)

    return keys_list


def get_keys_value_in_locale(guild_id: int, command_name: str) -> list:
    keys = get_keys_in_locale(guild_id, command_name)
    keys_value = []
    locale = get_guild_locale(guild_id)
    with open(f"./locales/{locale}.json", "r", encoding="utf-8") as file:
        locales_file = json.load(file)

    for key in keys:
        keys_value.append(locales_file[command_name][key])

    return keys_value


def get_localized_description(key: str) -> dict:
    descs = []
    for locale in LOCALE_LIST:
        with open(f"./locales/{locale}.json", "r", encoding="utf-8") as file:
            locales_file = json.load(file)

        descs.append(locales_file[key]["description"])

    return {"ru": descs[0], "en-US": descs[1]}


def get_localized_name(key: str) -> dict:
    names = []
    for locale in LOCALE_LIST:
        with open(f"./locales/{locale}.json", "r", encoding="utf-8") as file:
            locales_file = json.load(file)

        names.append(locales_file[key]["name"])

    return {"ru": names[0], "en-US": names[1]}
