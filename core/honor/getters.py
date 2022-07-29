import sqlite3


def get_user_honor_points(user_id: int) -> int:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    honor_points = \
        cursor.execute(f"SELECT honor_points FROM honor WHERE user_id = {user_id}").fetchone()[0]
    cursor.close()
    db.close()
    return honor_points


def get_user_honor_level(user_id: int) -> int:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    honor_level = \
        cursor.execute(f"SELECT honor_level FROM honor WHERE user_id = {user_id}").fetchone()[0]
    cursor.close()
    db.close()
    return honor_level


def get_rome_symbol(number: int) -> str:
    if number > 5:
        number = 5
    rome_number = {
        1: "I",
        2: "II",
        3: "III",
        4: "IV",
        5: "V"
    }
    return rome_number[number]
