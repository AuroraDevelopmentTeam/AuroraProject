import sqlite3
from core.checkers import is_guild_id_in_table, is_user_in_table
from config import settings
from core.locales.getters import get_msg_from_locale_by_key


def write_in_loggers_standart_values(guilds) -> None:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    for guild in guilds:
        if is_guild_id_in_table("loggers", guild.id) is False:
            sql = (
                "INSERT INTO loggers(guild_id, log_channel_id, "
                "logs_enabled) VALUES (?, ?, ?)"
            )
            val = (
                guild.id,
                0,
                settings['default_logs_enabled']
            )
            cursor.execute(sql, val)
            db.commit()
    cursor.close()
    db.close()
    return
