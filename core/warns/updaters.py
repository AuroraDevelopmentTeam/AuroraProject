import sqlite3


def remove_warn_from_table(warn_id: int, guild_id: int, user_id: int) -> None:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    cursor.execute(f"DELETE FROM warns WHERE warn_id = {warn_id} AND guild_id = {guild_id} AND user_id = {user_id}")
    db.commit()
    cursor.close()
    db.commit()
    return
