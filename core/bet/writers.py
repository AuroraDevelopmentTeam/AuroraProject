import sqlite3
from core.checkers import is_guild_id_in_table, is_user_in_table


def write_in_bets_standart_values(guilds) -> None:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    for guild in guilds:
        if is_guild_id_in_table("bets", guild.id) is False:
            sql = (
                "INSERT INTO bets(guild_id, min_bet, max_bet) VALUES (?, ?, ?)"
            )
            val = (
                guild.id,
                1,
                1000000
            )
            cursor.execute(sql, val)
            db.commit()
    cursor.close()
    db.close()
    return
