import sqlite3
from core.money.getters import get_user_balance


def update_guild_currency_symbol(guild_id: int, currency_symbol: str) -> None:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    sql = "UPDATE money_config SET guild_currency = ? WHERE guild_id = ?"
    values = (currency_symbol, guild_id)
    cursor.execute(sql, values)
    db.commit()
    cursor.close()
    db.close()
    return


def update_guild_starting_balance(guild_id: int, balance: int) -> None:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    sql = "UPDATE money_config SET guild_starting_balance = ? WHERE guild_id = ?"
    values = (balance, guild_id)
    cursor.execute(sql, values)
    db.commit()
    cursor.close()
    db.close()
    return


def update_guild_payday_amount(guild_id: int, payday_amount: int) -> None:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    sql = "UPDATE money_config SET guild_payday_amount = ? WHERE guild_id = ?"
    values = (payday_amount, guild_id)
    cursor.execute(sql, values)
    db.commit()
    cursor.close()
    db.close()
    return


def update_user_balance(guild_id: int, user_id: int, money: int) -> None:
    balance = get_user_balance(guild_id, user_id)
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    sql = "UPDATE money SET balance = ? WHERE guild_id = ? AND user_id = ?"
    values = (balance + money, guild_id, user_id)
    cursor.execute(sql, values)
    db.commit()
    cursor.close()
    db.close()
    return


def set_user_balance(guild_id: int, user_id: int, money: int) -> None:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    sql = "UPDATE money SET balance = ? WHERE guild_id = ? AND user_id = ?"
    values = (money, guild_id, user_id)
    cursor.execute(sql, values)
    db.commit()
    cursor.close()
    db.close()
    return
