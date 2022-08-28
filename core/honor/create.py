import sqlite3


def create_honor_table() -> None:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    cursor.execute(
        f"""CREATE TABLE IF NOT EXISTS honor (
        user_id INTEGER, honor_level INTEGER, honor_points INTEGER
    )"""
    )
    db.commit()
    cursor.close()
    db.close()
    return
