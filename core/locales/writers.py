import sqlite3
from core.checkers import is_guild_id_in_table


def write_in_locales_standart_values(guilds) -> None:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    for guild in guilds:
        if is_guild_id_in_table("locales", guild.id) is False:
            sql = "INSERT INTO locales(guild_id, locale) VALUES (?, ?)"
            val = (guild.id, settings['default_locale'])
            cursor.execute(sql, val)
            db.commit()
    cursor.close()
    db.close()
    return