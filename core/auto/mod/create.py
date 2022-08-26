import sqlite3


def create_mod_word_table() -> None:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    cursor.execute(
        f"""CREATE TABLE IF NOT EXISTS mod_word (guild_id INTERGER, word TEXT)"""
    )
    db.commit()
    cursor.close()
    db.close()
    return


def create_mod_config_table() -> None:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    cursor.execute(
        f"""CREATE TABLE IF NOT EXISTS mod_config (guild_id INTERGER, word_detect BOOL, link_detect BOOL, 
        nickname_detect BOOL, status_detect BOOL, guild_moderation_mode TEXT) """
    )
    db.commit()
    cursor.close()
    db.close()
    return
