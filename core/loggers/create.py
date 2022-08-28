import sqlite3


def create_loggers_table() -> None:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    cursor.execute(
        f"""CREATE TABLE IF NOT EXISTS loggers (
        guild_id INTEGER, log_channel_id INTEGER, logs_enabled BOOL
    )"""
    )
    db.commit()
    cursor.close()
    db.close()
    return
