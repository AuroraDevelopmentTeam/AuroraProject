import sqlite3
from easy_pil import *
import nextcord

from core.embeds import construct_basic_embed
from core.checkers import is_guild_id_in_table, is_user_in_table


def create_level_table() -> None:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    cursor.execute(
        f"""CREATE TABLE IF NOT EXISTS levels (
        guild_id INTEGER, user_id INTEGER, level INTEGER, exp INTEGER
    )"""
    )
    db.commit()
    cursor.close()
    db.close()
    return


def create_level_config_table() -> None:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    cursor.execute(
        f"""CREATE TABLE IF NOT EXISTS levels_config (
        guild_id INTEGER, min_exp_per_message INTEGER, max_exp_per_message INTEGER, level_up_messages_state BOOLEAN
    )"""
    )
    db.commit()
    cursor.close()
    db.close()
    return
