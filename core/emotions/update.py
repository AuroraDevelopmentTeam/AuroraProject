import sqlite3


def update_emotions_for_money_state(guild_id: int, state: bool) -> None:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    sql = "UPDATE emotions_cost SET emotions_for_money_state = ? WHERE guild_id = ?"
    values = (state, guild_id)
    cursor.execute(sql, values)
    db.commit()
    cursor.close()
    db.close()
    return


def update_emotions_cost(guild_id: int, cost: int) -> None:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    sql = "UPDATE emotions_cost SET cost = ? WHERE guild_id = ?"
    values = (cost, guild_id)
    cursor.execute(sql, values)
    db.commit()
    cursor.close()
    db.close()
    return
