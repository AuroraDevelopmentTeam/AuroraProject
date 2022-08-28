import sqlite3


def update_server_clan_icon(guild_id: int, clan_id: int, icon_url: str) -> None:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    sql = "UPDATE clans SET icon = ? WHERE guild_id = ? AND clan_id = ?"
    values = (pair_id, guild_id, user_id)
    cursor.execute(sql, values)
    db.commit()
    cursor.close()
    db.close()
    return
