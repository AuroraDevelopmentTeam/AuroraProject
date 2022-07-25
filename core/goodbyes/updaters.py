import sqlite3


def set_goodbye_channel(guild_id: int, goodbye_channel_id: int) -> None:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    sql = "UPDATE goodbye_config SET goodbye_message_channel = ? WHERE guild_id = ?"
    values = (goodbye_channel_id, guild_id)
    cursor.execute(sql, values)
    db.commit()
    cursor.close()
    db.close()
    return


def set_goodbye_message_state(guild_id: int, goodbye_message_enabled: bool) -> None:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    sql = "UPDATE goodbye_config SET goodbye_message_enabled = ? WHERE guild_id = ?"
    values = (goodbye_message_enabled, guild_id)
    cursor.execute(sql, values)
    db.commit()
    cursor.close()
    db.close()
    return


def update_goodbye_message_type(guild_id: int, goodbye_message_type: str) -> None:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    sql = "UPDATE goodbye_config SET goodbye_message_type = ? WHERE guild_id = ?"
    values = (goodbye_message_type, guild_id)
    cursor.execute(sql, values)
    db.commit()
    cursor.close()
    db.close()
    return


def update_goodbye_message_title(guild_id: int, goodbye_message_title: str) -> None:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    sql = "UPDATE goodbye_config SET goodbye_message_title = ? WHERE guild_id = ?"
    values = (goodbye_message_title, guild_id)
    cursor.execute(sql, values)
    db.commit()
    cursor.close()
    db.close()
    return


def update_goodbye_message_description(guild_id: int, goodbye_message_description: str) -> None:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    sql = "UPDATE goodbye_config SET goodbye_message_description = ? WHERE guild_id = ?"
    values = (goodbye_message_description, guild_id)
    cursor.execute(sql, values)
    db.commit()
    cursor.close()
    db.close()
    return


def update_goodbye_message_url(guild_id: int, goodbye_message_url: str) -> None:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    sql = "UPDATE goodbye_config SET goodbye_message_url = ? WHERE guild_id = ?"
    values = (goodbye_message_url, guild_id)
    cursor.execute(sql, values)
    db.commit()
    cursor.close()
    db.close()
    return