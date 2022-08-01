import sqlite3


def check_warn(guild_id, warn_id):
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    if cursor.execute(
            f"SELECT warn_id FROM warns WHERE guild_id = {guild_id} AND warn_id = {warn_id}").fetchone() is None:
        cursor.close()
        db.close()
        return False
    else:
        cursor.close()
        db.close()
        return True
