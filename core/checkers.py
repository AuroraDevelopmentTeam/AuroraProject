import sqlite3
import nextcord


def is_guild_id_in_table(table_name: str, guild_id: int) -> bool:
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


def is_locale_valid(locale: str) -> bool:
    locales = ["en_us", "ru_ru"]
    if locale in locales:
        return True
    else:
        return False


def is_user_in_table(table_name, guild_id, user_id):
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    if cursor.execute(f"SELECT user_id FROM {table_name} WHERE guild_id = {guild_id} "
                      f"AND user_id = {user_id}").fetchone() is None:
        cursor.close()
        db.close()
        return False
    else:
        cursor.close()
        db.close()
        return True


def is_str_or_emoji(symbol):
    if isinstance(symbol, str) or isinstance(symbol, nextcord.Emoji):
        return True
    else:
        return False
