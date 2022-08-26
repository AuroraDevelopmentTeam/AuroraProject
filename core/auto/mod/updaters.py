import sqlite3


def update_server_word_detect(guild_id: int, word_detect_state: bool) -> None:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    sql = "UPDATE mod_config SET word_detect = ? WHERE guild_id = ?"
    values = (word_detect_state, guild_id)
    cursor.execute(sql, values)
    db.commit()
    cursor.close()
    db.close()
    return


def update_server_link_detect(guild_id: int, link_detect_state: bool) -> None:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    sql = "UPDATE mod_config SET link_detect = ? WHERE guild_id = ?"
    values = (link_detect_state, guild_id)
    cursor.execute(sql, values)
    db.commit()
    cursor.close()
    db.close()
    return


def update_server_nickname_detect(guild_id: int, nickname_detect_state: bool) -> None:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    sql = "UPDATE mod_config SET nickname_detect = ? WHERE guild_id = ?"
    values = (nickname_detect_state, guild_id)
    cursor.execute(sql, values)
    db.commit()
    cursor.close()
    db.close()
    return


def update_server_status_detect(guild_id: int, status_detect_state: bool) -> None:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    sql = "UPDATE mod_config SET status_detect = ? WHERE guild_id = ?"
    values = (status_detect_state, guild_id)
    cursor.execute(sql, values)
    db.commit()
    cursor.close()
    db.close()
    return


def update_server_moderation_mode(guild_id: int, moderation_mode: str) -> None:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    sql = "UPDATE mod_config SET guild_moderation_mode = ? WHERE guild_id = ?"
    values = (moderation_mode, guild_id)
    cursor.execute(sql, values)
    db.commit()
    cursor.close()
    db.close()
    return
