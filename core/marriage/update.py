import sqlite3

from core.locales.getters import get_msg_from_locale_by_key
from core.marriage.getters import get_divorce_counter


def update_user_pair(guild_id, user_id, pair_id) -> None:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    sql = "UPDATE marriage SET pair_id = ? WHERE guild_id = ? AND user_id = ?"
    values = (pair_id, guild_id, user_id)
    cursor.execute(sql, values)
    db.commit()
    cursor.close()
    db.close()


def update_user_like(guild_id: int, user_id: int, like_id: int) -> None:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    sql = "UPDATE marriage SET like_id = ? WHERE guild_id = ? AND user_id = ?"
    values = (like_id, guild_id, user_id)
    cursor.execute(sql, values)
    db.commit()
    cursor.close()
    db.close()


def update_user_marriage_date(guild_id: int, user_id: int, date) -> None:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    sql = "UPDATE marriage SET date = ? WHERE guild_id = ? AND user_id = ?"
    values = (date, guild_id, user_id)
    cursor.execute(sql, values)
    db.commit()
    cursor.close()
    db.close()


def marry_users(guild_id: int, user_id: int, pair_id: int, date):
    db = sqlite3.connect("./databases/main.sqlite")
    default_love_description = get_msg_from_locale_by_key(guild_id, "default_love_description")
    cursor = db.cursor()
    update_user_pair(guild_id, user_id, pair_id)
    update_user_pair(guild_id, pair_id, user_id)
    update_user_love_description(guild_id, user_id, default_love_description)
    update_user_love_description(guild_id, pair_id, default_love_description)
    update_user_marriage_date(guild_id, user_id, date)
    update_user_marriage_date(guild_id, pair_id, date)
    cursor.close()
    db.close()


def divorce_users(guild_id: int, user_id: int, pair_id: int) -> None:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    update_user_pair(guild_id, user_id, 0)
    update_user_pair(guild_id, pair_id, 0)
    increment_user_divorces(guild_id, user_id)
    increment_user_divorces(guild_id, pair_id)
    update_user_love_description(guild_id, user_id, "0")
    update_user_love_description(guild_id, pair_id, "0")
    update_user_marriage_date(guild_id, user_id, "0")
    update_user_marriage_date(guild_id, pair_id, "0")
    cursor.close()
    db.close()


def increment_user_divorces(guild_id: int, user_id: int):
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    user_divorces = get_divorce_counter(guild_id, user_id)
    sql = "UPDATE marriage SET divorces = ? WHERE guild_id = ? AND user_id = ?"
    values = (user_divorces + 1, guild_id, user_id)
    cursor.execute(sql, values)
    db.commit()
    cursor.close()
    db.close()


def update_user_love_description(guild_id: int, user_id: int, description: str):
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    sql = "UPDATE marriage SET love_description = ? WHERE guild_id = ? AND user_id = ?"
    values = (description, guild_id, user_id)
    cursor.execute(sql, values)
    db.commit()
    cursor.close()
    db.close()
