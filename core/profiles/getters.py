import sqlite3


def get_profile_description(user_id: int) -> str:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    description = \
        cursor.execute(f"SELECT description FROM profiles WHERE user_id = {user_id}").fetchone()[0]
    cursor.close()
    db.close()
    return description


def get_avatar_form(user_id: int) -> str:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    avatar_form = \
        cursor.execute(f"SELECT avatar_form FROM profiles WHERE user_id = {user_id}").fetchone()[0]
    cursor.close()
    db.close()
    return avatar_form
