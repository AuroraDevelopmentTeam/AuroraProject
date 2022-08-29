import sqlite3


def create_shop_table() -> None:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS shop (
        guild_id INTEGER, role_id INTEGER, cost INTEGER
    )"""
    )
    db.commit()
    cursor.close()
    db.close()
    return


def create_custom_shop_table() -> None:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS custom_shop ( guild_id INTEGER, role_id INTEGER, cost INTEGER, 
        owner_id INTEGER, created INTEGER, expiration_date INTEGER, bought INTEGER ) """
    )
    db.commit()
    cursor.close()
    db.close()
    return
