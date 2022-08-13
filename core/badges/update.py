import sqlite3


def update_user_badge_state(guild_id: int, user_id: int, badge: str, state: bool) -> None:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    sql = f"UPDATE badges SET {badge} = ? WHERE guild_id = ? AND user_id = ?"
    values = (state, guild_id, user_id)
    cursor.execute(sql, values)
    db.commit()
    cursor.close()
    db.close()
    return
