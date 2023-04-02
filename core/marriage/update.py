import sqlite3

from core.locales.getters import get_msg_from_locale_by_key
from core.marriage.getters import (
    get_divorce_counter,
    get_user_gifts_price,
    get_user_gift_counter,
    get_family_money,
    get_user_loveroom_id
)
from core.money.updaters import update_user_balance


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


def update_user_loveroom_expire_date(guild_id: int, user_id: int, loveroom_expire_date: int) -> None:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    sql = "UPDATE marriage SET loveroom_expire = ? WHERE guild_id = ? AND user_id = ?"
    values = (loveroom_expire_date, guild_id, user_id)
    cursor.execute(sql, values)
    db.commit()
    cursor.close()
    db.close()
    return


def update_user_loveroom_id(guild_id: int, user_id: int, loveroom_id: int) -> None:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    sql = "UPDATE marriage SET loveroom_id = ? WHERE guild_id = ? AND user_id = ?"
    values = (loveroom_id, guild_id, user_id)
    cursor.execute(sql, values)
    db.commit()
    cursor.close()
    db.close()
    return


def marry_users(guild_id: int, user_id: int, pair_id: int, date):
    default_love_description = get_msg_from_locale_by_key(
        guild_id, "default_love_description"
    )
    update_user_pair(guild_id, user_id, pair_id)
    update_user_pair(guild_id, pair_id, user_id)
    update_user_love_description(guild_id, user_id, default_love_description)
    update_user_love_description(guild_id, pair_id, default_love_description)
    update_user_marriage_date(guild_id, user_id, date)
    update_user_marriage_date(guild_id, pair_id, date)
    set_couple_family_money(guild_id, user_id, pair_id, 0)
    return


def divorce_users(guild_id: int, user_id: int, pair_id: int) -> None:
    update_user_pair(guild_id, user_id, 0)
    update_user_pair(guild_id, pair_id, 0)
    increment_user_divorces(guild_id, user_id)
    increment_user_divorces(guild_id, pair_id)
    update_user_love_description(guild_id, user_id, "0")
    update_user_love_description(guild_id, pair_id, "0")
    update_user_marriage_date(guild_id, user_id, "0")
    update_user_marriage_date(guild_id, pair_id, "0")
    family_money = get_family_money(guild_id, user_id)
    update_user_balance(guild_id, user_id, int(family_money / 2))
    update_user_balance(guild_id, pair_id, int(family_money / 2))
    set_couple_family_money(guild_id, user_id, pair_id, 0)
    update_user_loveroom_expire_date(guild_id, user_id, 0)
    update_user_loveroom_expire_date(guild_id, pair_id, 0)
    update_user_loveroom_id(guild_id, user_id, 0)
    update_user_loveroom_id(guild_id, user_id, 0)

    return


def increment_user_divorces(guild_id: int, user_id: int) -> None:
    user_divorces = get_divorce_counter(guild_id, user_id)
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
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
    gift_counter = get_user_gift_counter(guild_id, user_id, gift)
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    sql = f"UPDATE gifts SET {gift} = ? WHERE guild_id = ? AND user_id = ?"
    values = (gift_counter + amount, guild_id, user_id)
    cursor.execute(sql, values)
    db.commit()
    cursor.close()
    db.close()
    return


def set_user_gift_count(guild_id: int, user_id: int, gift: str, amount: int) -> None:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    sql = f"UPDATE gifts SET {gift} = ? WHERE guild_id = ? AND user_id = ?"
    values = (amount, guild_id, user_id)
    cursor.execute(sql, values)
    db.commit()
    cursor.close()
    db.close()
    return


def update_user_gift_price(guild_id: int, user_id: int, price: int) -> None:
    gift_price = get_user_gifts_price(guild_id, user_id)
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    sql = f"UPDATE gifts SET gift_price = ? WHERE guild_id = ? AND user_id = ?"
    values = (gift_price + price, guild_id, user_id)
    cursor.execute(sql, values)
    db.commit()
    cursor.close()
    db.close()
    return


def set_user_gift_price(guild_id: int, user_id: int, price: int) -> None:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    sql = f"UPDATE gifts SET gift_price = ? WHERE guild_id = ? AND user_id = ?"
    values = (price, guild_id, user_id)
    cursor.execute(sql, values)
    db.commit()
    cursor.close()
    db.close()
    return


def set_user_family_money(guild_id: int, user_id: int, amount: int) -> None:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    sql = f"UPDATE marriage SET family_money = ? WHERE guild_id = ? AND user_id = ?"
    values = (amount, guild_id, user_id)
    cursor.execute(sql, values)
    db.commit()
    cursor.close()
    db.close()
    return


def update_user_family_money(guild_id: int, user_id: int, amount: int) -> None:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    family_money = get_family_money(guild_id, user_id)
    sql = f"UPDATE marriage SET family_money = ? WHERE guild_id = ? AND user_id = ?"
    values = (family_money + amount, guild_id, user_id)
    cursor.execute(sql, values)
    db.commit()
    cursor.close()
    db.close()
    return


def set_couple_family_money(
        guild_id: int, user_id: int, pair_id: int, amount: int
) -> None:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    set_user_family_money(guild_id, user_id, amount)
    set_user_family_money(guild_id, pair_id, amount)
    db.commit()
    cursor.close()
    db.close()
    return


def update_couple_family_money(
        guild_id: int, user_id: int, pair_id: int, amount: int
) -> None:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    update_user_family_money(guild_id, user_id, amount)
    update_user_family_money(guild_id, pair_id, amount)
    db.commit()
    cursor.close()
    db.close()
    return


def update_marriage_config_enable_loverooms(guild_id: int, loveroom_state: bool) -> None:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    sql = f"UPDATE marriage_config SET enable_loverooms = ? WHERE guild_id = ?"
    values = (loveroom_state, guild_id)
    cursor.execute(sql, values)
    db.commit()
    cursor.close()
    db.close()
    return


def update_marriage_config_marriage_price(guild_id: int, marriage_price: int) -> None:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    sql = f"UPDATE marriage_config SET marriage_price = ? WHERE guild_id = ?"
    values = (marriage_price, guild_id)
    cursor.execute(sql, values)
    db.commit()
    cursor.close()
    db.close()
    return


def update_marriage_config_month_loveroom_price(guild_id: int, month_loveroom_price: int) -> None:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    sql = f"UPDATE marriage_config SET month_loveroom_price = ? WHERE guild_id = ?"
    values = (month_loveroom_price, guild_id)
    cursor.execute(sql, values)
    db.commit()
    cursor.close()
    db.close()
    return


def update_marriage_config_loveroom_category(guild_id: int, loveroom_category: int) -> None:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    sql = f"UPDATE marriage_config SET loveroom_category = ? WHERE guild_id = ?"
    values = (loveroom_category, guild_id)
    cursor.execute(sql, values)
    db.commit()
    cursor.close()
    db.close()
    return
