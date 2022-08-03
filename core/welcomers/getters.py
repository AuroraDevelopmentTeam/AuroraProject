import sqlite3


def get_server_welcome_channel_id(guild_id: int) -> int:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    welcome_channel_id = cursor.execute(
        f"SELECT welcome_message_channel FROM welcomers_config WHERE guild_id = {guild_id}"
    ).fetchone()[0]
    cursor.close()
    db.close()
    return welcome_channel_id


def get_server_welcome_state(guild_id: int) -> bool:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    messages_state = cursor.execute(
        f"SELECT welcome_message_enabled FROM welcomers_config WHERE guild_id = {guild_id}"
    ).fetchone()[0]
    cursor.close()
    db.close()
    return bool(messages_state)


def get_server_welcome_message_type(guild_id: int) -> str:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    messages_type = cursor.execute(
        f"SELECT welcome_message_type FROM welcomers_config WHERE guild_id = {guild_id}"
    ).fetchone()[0]
    cursor.close()
    db.close()
    return messages_type
