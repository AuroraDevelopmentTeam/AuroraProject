import sqlite3


def get_user_level(guild_id: int, user_id: int) -> int:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    level = \
        cursor.execute(f"SELECT level FROM levels WHERE guild_id = {guild_id} AND user_id = {user_id}").fetchone()[0]
    cursor.close()
    db.close()
    return level


def get_user_exp(guild_id: int, user_id: int) -> int:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    exp = \
        cursor.execute(f"SELECT exp FROM levels WHERE guild_id = {guild_id} AND user_id = {user_id}").fetchone()[0]
    cursor.close()
    db.close()
    return exp


def get_min_max_exp(guild_id: int) -> tuple[int, int]:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    min_exp = cursor.execute(f"SELECT min_exp_per_message FROM levels_config WHERE guild_id = {guild_id}").fetchone()[0]
    max_exp = cursor.execute(f"SELECT max_exp_per_message FROM levels_config WHERE guild_id = {guild_id}").fetchone()[0]
    cursor.close()
    db.close()
    return min_exp, max_exp


def get_guild_messages_state(guild_id: int) -> bool:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    messages_state = \
        cursor.execute(f"SELECT level_up_messages_state FROM levels_config WHERE guild_id = {guild_id}").fetchone()[0]
    cursor.close()
    db.close()
    return bool(messages_state)