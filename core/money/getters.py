import sqlite3


def get_user_balance(guild_id: int, user_id: int) -> int:
    db = sqlite3.connect("./databases/main.sqlite")
    print(db)
    cursor = db.cursor()
    print(cursor)
    balance = cursor.execute(
        f"SELECT balance FROM money WHERE guild_id = {guild_id} AND user_id = {user_id}"
    ).fetchone()[0]
    cursor.close()
    db.close()
    return balance


def get_guild_currency_symbol(guild_id: int) -> str:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    currency_symbol = cursor.execute(
        f"SELECT guild_currency FROM money_config" f" WHERE guild_id = {guild_id}"
    ).fetchone()[0]
    cursor.close()
    db.close()
    return currency_symbol


def get_guild_starting_balance(guild_id: int) -> int:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    starting_balance = cursor.execute(
        f"SELECT guild_starting_balance FROM money_config"
        f" WHERE guild_id = {guild_id}"
    ).fetchone()[0]
    cursor.close()
    db.close()
    return starting_balance


def get_guild_payday_amount(guild_id: int) -> int:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    payday_amount = cursor.execute(
        f"SELECT guild_payday_amount FROM money_config" f" WHERE guild_id = {guild_id}"
    ).fetchone()[0]
    cursor.close()
    db.close()
    return payday_amount


def get_guild_min_max_msg_income(guild_id: int) -> list[int, int]:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    income = cursor.execute(
        f"SELECT min_msg_income, max_msg_income FROM chat_money_config"
        f" WHERE guild_id = {guild_id}"
    ).fetchone()
    min_income = income[0]
    max_income = income[1]
    cursor.close()
    db.close()
    return [min_income, max_income]


def get_msg_cooldown(guild_id: int) -> int:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    msg_cooldown = cursor.execute(
        f"SELECT msg_cooldown FROM chat_money_config" f" WHERE guild_id = {guild_id}"
    ).fetchone()[0]
    cursor.close()
    db.close()
    return msg_cooldown


def get_guild_min_max_voice_income(guild_id: int) -> list[int, int]:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    income = cursor.execute(
        f"SELECT min_voice_income, max_voice_income FROM chat_money_config"
        f" WHERE guild_id = {guild_id}"
    ).fetchone()
    min_income = income[0]
    max_income = income[1]
    cursor.close()
    db.close()
    return [min_income, max_income]


def get_voice_minutes_for_income(guild_id: int) -> int:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    voice_minutes = cursor.execute(
        f"SELECT voice_minutes_for_money FROM chat_money_config"
        f" WHERE guild_id = {guild_id}"
    ).fetchone()[0]
    cursor.close()
    db.close()
    return voice_minutes


def get_channel_income_state(guild_id: int, channel_id: int) -> bool:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    messages_state = cursor.execute(
        f"SELECT enabled FROM money_channels_config WHERE guild_id = {guild_id} AND channel_id = {channel_id}"
    ).fetchone()
    cursor.close()
    db.close()
    if messages_state is None:
        return True
    else:
        state = messages_state[0]
        return bool(state)


def list_income_roles(guild_id: int):
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    rows = cursor.execute(
        f"SELECT role_id, income FROM roles_money WHERE guild_id = {guild_id}"
    ).fetchall()
    cursor.close()
    db.close()
    return rows
