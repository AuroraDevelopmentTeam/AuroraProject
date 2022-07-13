import sqlite3


def update_guild_locale(locale: str, guild_id: int) -> None:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    sql = "UPDATE locales SET locale = ? WHERE guild_id = ?"
    values = (locale, guild_id)
    cursor.execute(sql, values)
    db.commit()
    cursor.close()
    db.close()
    return