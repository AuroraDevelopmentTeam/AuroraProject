import sqlite3


def get_min_bet(guild_id: int) -> int:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    min_bet = cursor.execute(
        f"SELECT min_bet FROM bets WHERE guild_id = {guild_id}"
    ).fetchone()[0]
    db.commit()
    cursor.close()
    db.close()
    return min_bet


def get_max_bet(guild_id: int) -> int:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    min_bet = cursor.execute(
        f"SELECT max_bet FROM bets WHERE guild_id = {guild_id}"
    ).fetchone()[0]
    db.commit()
    cursor.close()
    db.close()
    return min_bet
