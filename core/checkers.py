import sqlite3


def is_guild_id_in_table(table_name, guild_id) -> bool:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    if cursor.execute(f"SELECT guild_id FROM {table_name} WHERE guild_id = {guild_id}").fetchone() is None:
        cursor.close()
        db.close()
        return False
    else:
        cursor.close()
        db.close()
        return True


def is_locale_valid(locale) -> bool:
    locales = ["en_us", "ru_ru"]
    if locale in locales:
        return True
    else:
        return False
