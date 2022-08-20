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


def create_level_autorole_table() -> None:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    cursor.execute(
        f"""CREATE TABLE IF NOT EXISTS autoroles_level ( guild_id INTERGER, level INTERGER, 
    autorole_id INTERGER)"""
    )
    db.commit()
    cursor.close()
    db.close()
    return


def create_reaction_autorole_table() -> None:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    cursor.execute(
        f"""CREATE TABLE IF NOT EXISTS reaction_autorole (guild_id INTERGER, channel_id INTERGER, message_id INTERGER, 
    reaction TEXT, autorole_id INTERGER, is_custom BOOL)"""
    )
    db.commit()
    cursor.close()
    db.close()
    return
