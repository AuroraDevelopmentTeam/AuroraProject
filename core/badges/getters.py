import sqlite3


def get_user_badge_state(guild_id: int, user_id: int, badge: str) -> bool:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    badge_state = cursor.execute(
        f"SELECT {badge} FROM badges WHERE guild_id = {guild_id} AND user_id = {user_id}"
    ).fetchone()[0]
    cursor.close()
    db.close()
    return bool(badge_state)
