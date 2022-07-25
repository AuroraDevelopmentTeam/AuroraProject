import sqlite3
import nextcord

from core.marriage.getters import get_user_pair_id


def is_guild_id_in_table(table_name: str, guild_id: int) -> bool:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    if cursor.execute(f"SELECT guild_id FROM {table_name} WHERE guild_id = {guild_id}").fetchone() is None:
        cursor.close()
        db.close()
        return False
    else:
        cursor.close()
        db.close()
        return True


def is_warn_id_in_table(table_name: str, warn_id: int, guild_id: int, user_id: int) -> bool:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    if cursor.execute(f"SELECT warn_id FROM {table_name} WHERE warn_id = {warn_id} "
                      f"AND guild_id = {guild_id} AND user_id = {user_id}").fetchone() is None:
        cursor.close()
        db.close()
        return False
    else:
        cursor.close()
        db.close()
        return True


def is_locale_valid(locale: str) -> bool:
    locales = ["en_us", "ru_ru"]
    if locale in locales:
        return True
    else:
        return False


def is_user_in_table(table_name, guild_id, user_id) -> bool:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    if cursor.execute(f"SELECT user_id FROM {table_name} WHERE guild_id = {guild_id} "
                      f"AND user_id = {user_id}").fetchone() is None:
        cursor.close()
        db.close()
        return False
    else:
        cursor.close()
        db.close()
        return True


def is_str_or_emoji(symbol) -> bool:
    if isinstance(symbol, str) or isinstance(symbol, nextcord.Emoji):
        return True
    else:
        return False


def is_married(guild_id, user_id) -> bool:
    pair_id = get_user_pair_id(guild_id, user_id)
    if pair_id == 0:
        return False
    else:
        return True


def is_role_in_shop(guild_id, role_id) -> bool:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    if cursor.execute(f"SELECT role_id FROM shop WHERE guild_id = {guild_id} "
                      f"AND role_id = {role_id}").fetchone() is None:
        return False
    else:
        return True
