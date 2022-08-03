import sqlite3


def create_autoroles_table() -> None:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    cursor.execute(
        f"""CREATE TABLE IF NOT EXISTS autoroles ( guild_id INTERGER, autoroles_enabled BOOLEAN, 
    autorole_id INTERGER)"""
    )
    db.commit()
    cursor.close()
    db.close()
    return
