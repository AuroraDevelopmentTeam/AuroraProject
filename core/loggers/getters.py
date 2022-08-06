import sqlite3


def get_logging_channel(guild_id: int) -> int:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    log_channel_id = cursor.execute(
        f"SELECT log_channel_id FROM loggers WHERE guild_id = {guild_id}"
    ).fetchone()[0]
    cursor.close()
    db.close()
    return log_channel_id


def get_logging_state(guild_id: int) -> bool:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    logging_state = cursor.execute(
        f"SELECT logs_enabled FROM loggers WHERE guild_id = {guild_id}"
    ).fetchone()[0]
    cursor.close()
    db.close()
    return bool(logging_state)
