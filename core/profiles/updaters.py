import sqlite3


def update_profile_description(user_id: int, description: str) -> None:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    sql = "UPDATE profiles SET description = ? WHERE user_id = ?"
    values = (description, user_id)
    cursor.execute(sql, values)
    db.commit()
    cursor.close()
    db.close()
    return


def update_avatar_form(user_id: int, avatar_form: str) -> None:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    sql = "UPDATE profiles SET avatar_form = ? WHERE user_id = ?"
    values = (avatar_form, user_id)
    cursor.execute(sql, values)
    db.commit()
    cursor.close()
    db.close()
    return
