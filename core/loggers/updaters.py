import sqlite3


def update_logging_channel_id(guild_id: int, logging_channel_id: int) -> None:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    sql = "UPDATE loggers SET log_channel_id = ? WHERE guild_id = ?"
    values = (logging_channel_id, guild_id)
    cursor.execute(sql, values)
    db.commit()
    cursor.close()
    db.close()
    return


def update_logging_guild_state(guild_id: int, logging_state: bool) -> None:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    sql = "UPDATE loggers SET logs_enabled = ? WHERE guild_id = ?"
    values = (logging_state, guild_id)
    cursor.execute(sql, values)
    db.commit()
    cursor.close()
    db.close()
    return
