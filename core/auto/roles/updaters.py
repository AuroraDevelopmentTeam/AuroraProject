import sqlite3


def set_autoroles_state(guild_id: int, autoroles_enabled: bool) -> None:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    sql = "UPDATE autoroles SET autoroles_enabled = ? WHERE guild_id = ?"
    values = (autoroles_enabled, guild_id)
    cursor.execute(sql, values)
    db.commit()
    cursor.close()
    db.close()
    return
