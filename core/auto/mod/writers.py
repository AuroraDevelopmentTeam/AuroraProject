import sqlite3
from core.checkers import is_guild_id_in_table
from config import settings
from core.locales.getters import get_msg_from_locale_by_key


def write_in_mod_config_standart_values(guilds) -> None:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    for guild in guilds:
        if is_guild_id_in_table("mod_config", guild.id) is False:
            sql = (
                "INSERT INTO mod_config(guild_id, word_detect, "
                "link_detect, nickname_detect, status_detect, "
                "guild_moderation_mode) VALUES (?, ?, ?, ?, ?, ?)"
            )
            val = (
                guild.id,
                True,
                True,
                True,
                True,
                "community"
            )
            cursor.execute(sql, val)
            db.commit()
    cursor.close()
    db.close()
    return


def write_in_mod_word(guild_id: int, word: str) -> None:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    sql = "INSERT INTO mod_word(guild_id, word) VALUES (?, ?)"
    val = (guild_id, word)
    cursor.execute(sql, val)
    db.commit()
    cursor.close()
    db.close()


def delete_mod_word(guild_id: int, word: str) -> None:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    sql = f"DELETE FROM mod_word WHERE guild_id = {guild_id} AND word = '{word}'"
    val = (guild_id, word)
    cursor.execute(sql, val)
    db.commit()
    cursor.close()
    db.close()
