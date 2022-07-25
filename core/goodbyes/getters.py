import sqlite3


def get_server_goodbye_channel_id(guild_id: int) -> int:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    goodbye_channel_id = \
        cursor.execute(
            f"SELECT goodbye_message_channel FROM goodbye_config WHERE guild_id = {guild_id}").fetchone()[0]
    cursor.close()
    db.close()
    return goodbye_channel_id


def get_server_goodbye_state(guild_id: int) -> bool:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    messages_state = \
        cursor.execute(f"SELECT goodbye_message_enabled FROM goodbye_config WHERE guild_id = {guild_id}").fetchone()[
            0]
    cursor.close()
    db.close()
    return bool(messages_state)


def get_server_goodbye_message_type(guild_id: int) -> str:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    messages_type = \
        cursor.execute(f"SELECT goodbye_message_type FROM goodbye_config WHERE guild_id = {guild_id}").fetchone()[0]
    cursor.close()
    db.close()
    return messages_type
