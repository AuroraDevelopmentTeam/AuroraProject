import sqlite3


def get_user_balance(guild_id: int, user_id: int) -> int:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    balance = \
    cursor.execute(f"SELECT balance FROM money WHERE guild_id = {guild_id} AND user_id = {user_id}").fetchone()[0]
    cursor.close()
    db.close()
    return balance


def get_guild_currency_symbol(guild_id: int) -> str:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    currency_symbol = cursor.execute(f"SELECT guild_currency FROM money_config"
                                     f" WHERE guild_id = {guild_id}").fetchone()[0]
    cursor.close()
    db.close()
    return currency_symbol


def get_guild_starting_balance(guild_id: int) -> int:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    starting_balance = cursor.execute(f"SELECT guild_starting_balance FROM money_config"
                                      f" WHERE guild_id = {guild_id}").fetchone()[0]
    cursor.close()
    db.close()
    return starting_balance


def get_guild_payday_amount(guild_id: int) -> int:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    payday_amount = cursor.execute(f"SELECT guild_payday_amount FROM money_config"
                                   f" WHERE guild_id = {guild_id}").fetchone()[0]
    cursor.close()
    db.close()
    return payday_amount
