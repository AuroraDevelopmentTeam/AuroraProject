import sqlite3

from core.stats.getters import get_user_time_in_voice, get_user_messages_counter


def update_user_messages_counter(
    guild_id: int, user_id: int, messages_to_add: int
) -> None:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    messages_counter = get_user_messages_counter(guild_id, user_id)
    sql = "UPDATE stats SET messages = ? WHERE guild_id = ? AND user_id = ?"
    values = (messages_counter + messages_to_add, guild_id, user_id)
    cursor.execute(sql, values)
    db.commit()
    cursor.close()
    db.close()
    return


def update_user_time_in_voice(guild_id: int, user_id: int, time_to_add: int) -> None:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    voice_time = get_user_time_in_voice(guild_id, user_id)
    sql = "UPDATE stats SET in_voice = ? WHERE guild_id = ? AND user_id = ?"
    values = (voice_time + time_to_add, guild_id, user_id)
    cursor.execute(sql, values)
    db.commit()
    cursor.close()
    db.close()
    return


def update_user_join_time(guild_id: int, user_id: int, join_time: str) -> None:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    sql = "UPDATE stats SET join_time = ? WHERE guild_id = ? AND user_id = ?"
    values = (join_time, guild_id, user_id)
    cursor.execute(sql, values)
    db.commit()
    cursor.close()
    db.close()
    return
