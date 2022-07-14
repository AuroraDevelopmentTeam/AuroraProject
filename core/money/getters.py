import sqlite3


def get_user_balance(guild_id, user_id) -> int:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    balance = cursor.execute(f"SELECT balance FROM money WHERE guild_id = {guild_id} AND "
                             f"user_id = {user_id}").fetchone()[0]
    cursor.close()
    db.close()
    return balance


def get_guild_currency_symbol(guild_id) -> str:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    currency_symbol = cursor.execute(f"SELECT guild_currency FROM money_config"
                                     f" WHERE guild_id = {guild_id}").fetchone()[0]
    cursor.close()
    db.close()
    return currency_symbol