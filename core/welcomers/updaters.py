import sqlite3


def set_welcome_channel(guild_id: int, welcome_channel_id: int) -> None:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    sql = "UPDATE welcomers_config SET welcome_message_channel = ? WHERE guild_id = ?"
    values = (welcome_channel_id, guild_id)
    cursor.execute(sql, values)
    db.commit()
    cursor.close()
    db.close()
    return


def set_welcome_message_state(guild_id: int, welcome_message_enabled: bool) -> None:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    sql = "UPDATE welcomers_config SET welcome_message_enabled = ? WHERE guild_id = ?"
    values = (welcome_message_enabled, guild_id)
    cursor.execute(sql, values)
    db.commit()
    cursor.close()
    db.close()
    return


def update_welcome_message_type(guild_id: int, welcome_message_type: str) -> None:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    sql = "UPDATE welcomers_config SET welcome_message_type = ? WHERE guild_id = ?"
    values = (welcome_message_type, guild_id)
    cursor.execute(sql, values)
    db.commit()
    cursor.close()
    db.close()
    return


def update_welcome_message_title(guild_id: int, welcome_message_title: str) -> None:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    sql = "UPDATE welcomers_config SET welcome_message_title = ? WHERE guild_id = ?"
    values = (welcome_message_title, guild_id)
    cursor.execute(sql, values)
    db.commit()
    cursor.close()
    db.close()
    return


def update_welcome_message_description(
    guild_id: int, welcome_message_description: str
) -> None:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    sql = (
        "UPDATE welcomers_config SET welcome_message_description = ? WHERE guild_id = ?"
    )
    values = (welcome_message_description, guild_id)
    cursor.execute(sql, values)
    db.commit()
    cursor.close()
    db.close()
    return


def update_welcome_message_url(guild_id: int, welcome_message_url: str) -> None:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    sql = "UPDATE welcomers_config SET welcome_message_url = ? WHERE guild_id = ?"
    values = (welcome_message_url, guild_id)
    cursor.execute(sql, values)
    db.commit()
    cursor.close()
    db.close()
    return
