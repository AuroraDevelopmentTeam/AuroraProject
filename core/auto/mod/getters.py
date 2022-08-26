import sqlite3

import nextcord


def get_server_word_detect(guild_id: int) -> bool:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    word_detect = cursor.execute(
        f"SELECT word_detect FROM mod_config WHERE guild_id = {guild_id}"
    ).fetchone()[0]
    cursor.close()
    db.close()
    return bool(word_detect)


def get_server_link_detect(guild_id: int) -> bool:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    link_detect = cursor.execute(
        f"SELECT link_detect FROM mod_config WHERE guild_id = {guild_id}"
    ).fetchone()[0]
    cursor.close()
    db.close()
    return bool(link_detect)


def get_server_nickname_detect(guild_id: int) -> bool:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    nickname_detect = cursor.execute(
        f"SELECT nickname_detect FROM mod_config WHERE guild_id = {guild_id}"
    ).fetchone()[0]
    cursor.close()
    db.close()
    return bool(nickname_detect)


def get_server_status_detect(guild_id: int) -> bool:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    status_detect = cursor.execute(
        f"SELECT status_detect FROM mod_config WHERE guild_id = {guild_id}"
    ).fetchone()[0]
    cursor.close()
    db.close()
    return bool(status_detect)


def get_server_moderation_mode(guild_id: int) -> str:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    guild_moderation_mode = cursor.execute(
        f"SELECT guild_moderation_mode FROM mod_config WHERE guild_id = {guild_id}"
    ).fetchone()[0]
    cursor.close()
    db.close()
    return guild_moderation_mode


def fetchall_mod_words(guild_id: int) -> list[str]:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    mod_words = cursor.execute(
        f"SELECT word FROM mod_word WHERE guild_id = {guild_id}"
    ).fetchall()
    cursor.close()
    db.close()
    words = []
    for row in mod_words:
        words.append(row[0])
    return words
