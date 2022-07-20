import sqlite3
import random

from core.checkers import is_warn_id_in_table


def write_new_warn(guild_id, user_id, reason) -> None:
    warn_id = random.randint(1, 1000000000000000)
    while is_warn_id_in_table("warns", warn_id, guild_id, user_id) is True:
        warn_id = random.randint(1, 1000000000000000)
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    if is_warn_id_in_table("warns", warn_id, guild_id, user_id) is False:
        sql = "INSERT INTO warns(warn_id, guild_id, user_id, " \
                  "warn_reason) VALUES (?, ?, ?, ?)"
        val = (warn_id, guild_id, user_id, reason)
        cursor.execute(sql, val)
        db.commit()
    cursor.close()
    db.close()
    return
