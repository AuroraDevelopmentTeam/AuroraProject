import sqlite3
from core.checkers import is_guild_id_in_table
from config import settings


def write_in_locales_standart_values(guilds) -> None:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    for guild in guilds:
        if is_guild_id_in_table("locales", guild.id) is False:
            guild_locale = guild.preferred_locale
            if guild_locale is None:
                guild_locale = settings["default_locale"]
            elif guild_locale == "ru":
                guild_locale = "ru_ru"
            else:
                guild_locale = "en_us"
            sql = "INSERT INTO locales(guild_id, locale) VALUES (?, ?)"
            val = (guild.id, guild_locale)
            cursor.execute(sql, val)
            db.commit()
    cursor.close()
    db.close()
    return
