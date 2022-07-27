import sqlite3


def get_server_nitro_channel_id(guild_id: int) -> int:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    nitro_channel_id = \
        cursor.execute(
            f"SELECT nitro_message_channel FROM on_nitro_config WHERE guild_id = {guild_id}").fetchone()[0]
    cursor.close()
    db.close()
    return nitro_channel_id


def get_server_nitro_state(guild_id: int) -> bool:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    messages_state = \
        cursor.execute(f"SELECT nitro_message_enabled FROM on_nitro_config WHERE guild_id = {guild_id}").fetchone()[0]
    cursor.close()
    db.close()
    return bool(messages_state)
