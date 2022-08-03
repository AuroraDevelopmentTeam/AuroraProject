import sqlite3


def get_user_messages_counter(guild_id: int, user_id: int) -> int:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    messages_counter = \
        cursor.execute(f"SELECT messages FROM stats WHERE guild_id = {guild_id} AND user_id = {user_id}").fetchone()[0]
    cursor.close()
    db.close()
    return messages_counter


def get_user_time_in_voice(guild_id: int, user_id: int) -> int:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    in_voice = \
        cursor.execute(f"SELECT in_voice FROM stats WHERE guild_id = {guild_id} AND user_id = {user_id}").fetchone()[0]
    cursor.close()
    db.close()
    return in_voice


def get_user_join_time(guild_id: int, user_id: int) -> str:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    join_time = \
        cursor.execute(f"SELECT join_time FROM stats WHERE guild_id = {guild_id} AND user_id = {user_id}").fetchone()[0]
    cursor.close()
    db.close()
    return join_time
