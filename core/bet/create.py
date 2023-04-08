import random

import sqlite3
import nextcord


def create_bets_table() -> None:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS bets (guild_id INTEGER, min_bet INTEGER, max_bet INTEGER) """
    )
    db.commit()
    cursor.close()
    db.close()
    return
