import sqlite3

from core.honor.getters import get_user_honor_level, get_user_honor_points


def update_honor_points(user_id: int, honor_points_to_add: int) -> None:
    honor_points_now = get_user_honor_points(user_id)
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    sql = "UPDATE honor SET honor_points = ? WHERE user_id = ?"
    values = (honor_points_now + honor_points_to_add, user_id)
    cursor.execute(sql, values)
    db.commit()
    cursor.close()
    db.close()
    return


def update_honor_level(user_id: int, honor_levels_to_add: int) -> None:
    honor_level = get_user_honor_level(user_id)
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    sql = "UPDATE honor SET honor_level = ? WHERE user_id = ?"
    values = (honor_level + honor_levels_to_add, user_id)
    cursor.execute(sql, values)
    db.commit()
    cursor.close()
    db.close()
    return
