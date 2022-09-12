import sqlite3


def get_voice_creation_room(guild_id: int) -> int:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    voice_creation_room = cursor.execute(
        f"SELECT voice_creation_room_id FROM voice_private_config WHERE guild_id = {guild_id}"
    ).fetchone()[0]
    cursor.close()
    db.close()
    return voice_creation_room


def get_voice_controller_msg(guild_id: int) -> int:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    voice_controller_msg = cursor.execute(
        f"SELECT voice_controller_msg_id FROM voice_private_config WHERE guild_id = {guild_id}"
    ).fetchone()[0]
    cursor.close()
    db.close()
    return voice_controller_msg
