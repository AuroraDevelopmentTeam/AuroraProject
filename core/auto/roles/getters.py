import sqlite3


def get_server_autorole_state(guild_id: int) -> bool:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    autoroles_state = cursor.execute(
        f"SELECT autoroles_enabled FROM autoroles WHERE guild_id = {guild_id}"
    ).fetchone()[0]
    cursor.close()
    db.close()
    return bool(autoroles_state)


def get_server_autorole_id(guild_id: int) -> int:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    autorole_id = cursor.execute(
        f"SELECT autorole_id FROM autoroles WHERE guild_id = {guild_id}"
    ).fetchone()[0]
    cursor.close()
    db.close()
    return autorole_id
