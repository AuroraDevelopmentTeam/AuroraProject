import sqlite3


def check_warn(guild_id, warn_id):
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    if (
        cursor.execute(
            f"SELECT warn_id FROM warns WHERE guild_id = {guild_id} AND warn_id = {warn_id}"
        ).fetchone()
        is None
    ):
        cursor.close()
        db.close()
        return False
    else:
        cursor.close()
        db.close()
        return True


def get_warn_reason(guild_id: int, user_id: int) -> str:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    warn_reason = cursor.execute(
        f"SELECT warn_reason FROM warns WHERE guild_id = {guild_id} AND user_id = {user_id}"
    ).fetchone()[0]
    cursor.close()
    db.close()
    return warn_reason
