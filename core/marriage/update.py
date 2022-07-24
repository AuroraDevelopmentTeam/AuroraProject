import sqlite3

from core.locales.getters import get_msg_from_locale_by_key
from core.marriage.getters import get_divorce_counter, get_user_gifts_price, get_user_gift_counter


def update_user_pair(guild_id, user_id, pair_id) -> None:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    sql = "UPDATE marriage SET pair_id = ? WHERE guild_id = ? AND user_id = ?"
    values = (pair_id, guild_id, user_id)
    cursor.execute(sql, values)
    db.commit()
    cursor.close()
    db.close()
    return


def update_user_like(guild_id: int, user_id: int, like_id: int) -> None:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    sql = "UPDATE marriage SET like_id = ? WHERE guild_id = ? AND user_id = ?"
    values = (like_id, guild_id, user_id)
    cursor.execute(sql, values)
    db.commit()
    cursor.close()
    db.close()
    return


def update_user_marriage_date(guild_id: int, user_id: int, date) -> None:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    sql = "UPDATE marriage SET date = ? WHERE guild_id = ? AND user_id = ?"
    values = (date, guild_id, user_id)
    cursor.execute(sql, values)
    db.commit()
    cursor.close()
    db.close()
    return


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
    return


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
    return


def increment_user_divorces(guild_id: int, user_id: int) -> None:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    user_divorces = get_divorce_counter(guild_id, user_id)
    sql = "UPDATE marriage SET divorces = ? WHERE guild_id = ? AND user_id = ?"
    values = (user_divorces + 1, guild_id, user_id)
    cursor.execute(sql, values)
    db.commit()
    cursor.close()
    db.close()
    return


def update_user_love_description(guild_id: int, user_id: int, description: str) -> None:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    sql = "UPDATE marriage SET love_description = ? WHERE guild_id = ? AND user_id = ?"
    values = (description, guild_id, user_id)
    cursor.execute(sql, values)
    db.commit()
    cursor.close()
    db.close()
    return


def update_user_gift_count(guild_id: int, user_id: int, gift: str, amount: int) -> None:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    gift_counter = get_user_gift_counter(guild_id, user_id, gift)
    sql = f"UPDATE gifts SET {gift} = ? WHERE guild_id = ? AND user_id = ?"
    values = (gift_counter + amount, guild_id, user_id)
    cursor.execute(sql, values)
    db.commit()
    cursor.close()
    db.close()
    return


def update_user_gift_price(guild_id: int, user_id: int, price: int) -> None:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    gift_price = get_user_gifts_price(guild_id, user_id)
    sql = f"UPDATE gifts SET gift_price = ? WHERE guild_id = ? AND user_id = ?"
    values = (gift_price + price, guild_id, user_id)
    cursor.execute(sql, values)
    db.commit()
    cursor.close()
    db.close()
    return
