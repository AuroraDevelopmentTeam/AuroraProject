import sqlite3


def create_profiles_table() -> None:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    cursor.execute(
        f"""CREATE TABLE IF NOT EXISTS profiles (
        user_id INTEGER, description TEXT, avatar_form TEXT
    )"""
    )
    db.commit()
    cursor.close()
    db.close()
    return
