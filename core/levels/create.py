import sqlite3
from core.checkers import is_guild_id_in_table, is_user_in_table


def create_level_table() -> None:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    cursor.execute(f"""CREATE TABLE IF NOT EXISTS levels (
        guild_id INTERGER, user_id INTERGER, level INTERGER, exp INTERGER
    )""")
    db.commit()
    cursor.close()
    db.close()
    return


def create_level_config_table() -> None:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    cursor.execute(f"""CREATE TABLE IF NOT EXISTS levels_config (
        guild_id INTERGER, min_exp_per_message INTERGER, max_exp_per_message INTERGER, level_up_messages_state BOOLEAN
    )""")
    db.commit()
    cursor.close()
    db.close()
    return
