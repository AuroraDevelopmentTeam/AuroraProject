import sqlite3


def create_voice_private_config_table() -> None:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    cursor.execute(
        f"""CREATE TABLE IF NOT EXISTS voice_private_config (
        guild_id INTEGER, voice_creation_room_id INTEGER, voice_controller_msg_id INTEGER
    )"""
    )
    db.commit()
    cursor.close()
    db.close()
    return
