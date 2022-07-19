import random
import sqlite3

from core.levels.getters import get_user_exp, get_user_level


def update_user_exp(guild_id: int, user_id: int, min_exp: int, max_exp: int) -> None:
    if min_exp == max_exp:
        exp_to_add = min_exp
    else:
        exp_to_add = random.randint(min_exp, max_exp)
    exp_now = get_user_exp(guild_id, user_id)
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    sql = "UPDATE levels SET exp = ? WHERE guild_id = ? AND user_id = ?"
    values = (exp_now + exp_to_add, guild_id, user_id)
    cursor.execute(sql, values)
    db.commit()
    cursor.close()
    db.close()
    return


def update_user_level(guild_id: int, user_id: int, levels_to_add: int) -> None:
    level_now = get_user_level(guild_id, user_id)
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    sql = "UPDATE levels SET level = ? WHERE guild_id = ? AND user_id = ?"
    values = (level_now + levels_to_add, guild_id, user_id)
    cursor.execute(sql, values)
    db.commit()
    cursor.close()
    db.close()
    return


def set_user_exp_to_zero(guild_id: int, user_id: int) -> None:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    sql = "UPDATE levels SET exp = ? WHERE guild_id = ? AND user_id = ?"
    values = (0, guild_id, user_id)
    cursor.execute(sql, values)
    db.commit()
    cursor.close()
    db.close()
    return


def set_server_level_up_messages_state(guild_id: int, messages_state: bool) -> None:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    sql = "UPDATE levels_config SET level_up_messages_state = ? WHERE guild_id = ?"
    values = (messages_state, guild_id)
    cursor.execute(sql, values)
    db.commit()
    cursor.close()
    db.close()
    return
