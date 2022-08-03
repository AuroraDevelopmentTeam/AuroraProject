import sqlite3
import nextcord

from core.embeds import construct_basic_embed
from core.checkers import is_guild_id_in_table, is_user_in_table


def create_warns_table() -> None:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    cursor.execute(
        f"""CREATE TABLE IF NOT EXISTS warns (
        warn_id INTERGER, guild_id INTERGER, user_id INTERGER, warn_reason TEXT
    )"""
    )
    db.commit()
    cursor.close()
    db.close()
    return
