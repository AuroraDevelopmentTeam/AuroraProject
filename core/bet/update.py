import sqlite3


def update_min_bet(guild_id: int, min_bet: int) -> None:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    sql = "UPDATE bets SET min_bet = ? WHERE guild_id = ?"
    values = (min_bet, guild_id)
    cursor.execute(sql, values)
    db.commit()
    cursor.close()
    db.close()
    return


def update_max_bet(guild_id: int, max_bet: int) -> None:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    sql = "UPDATE bets SET max_bet = ? WHERE guild_id = ?"
    values = (max_bet, guild_id)
    cursor.execute(sql, values)
    db.commit()
    cursor.close()
    db.close()
    return
