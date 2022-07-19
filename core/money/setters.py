import sqlite3


def set_user_balance(guild_id: int, user_id: int, money: int) -> None:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    sql = "UPDATE money SET balance = ? WHERE guild_id = ? AND user_id = ?"
    values = (money, guild_id, user_id)
    cursor.execute(sql, values)
    db.commit()
    cursor.close()
    db.close()
    return