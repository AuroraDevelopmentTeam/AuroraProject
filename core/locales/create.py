import sqlite3
from core.checkers import is_guild_id_in_table
import json
from config import settings


def create_locales_table() -> None:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    cursor.execute(
        f"""CREATE TABLE IF NOT EXISTS locales (
        guild_id INTEGER, locale TEXT
    )"""
    )
    db.commit()
    cursor.close()
    db.close()
    return
