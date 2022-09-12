import sqlite3


def update_voice_creation_room(guild_id: int, voice_creation_room_id: int) -> None:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    sql = "UPDATE voice_private_config SET voice_creation_room_id = ? WHERE guild_id = ?"
    values = (voice_creation_room_id, guild_id)
    cursor.execute(sql, values)
    db.commit()
    cursor.close()
    db.close()
    return


def update_voice_controller_msg(guild_id: int, voice_controller_msg_id: int) -> None:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    sql = "UPDATE voice_private_config SET voice_controller_msg_id = ? WHERE guild_id = ?"
    values = (voice_controller_msg_id, guild_id)
    cursor.execute(sql, values)
    db.commit()
    cursor.close()
    db.close()
    return
