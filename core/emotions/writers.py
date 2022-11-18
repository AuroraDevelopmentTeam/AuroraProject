import sqlite3
from core.checkers import is_guild_id_in_table, is_user_in_table


def write_in_emotions_cost_standart_values(guilds) -> None:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    for guild in guilds:
        if is_guild_id_in_table("emotions_cost", guild.id) is False:
            sql = (
                "INSERT INTO emotions_cost(guild_id, emotions_for_money_state, cost) VALUES (?, ?, ?)"
            )
            val = (
                guild.id,
                False,
                0
            )
            cursor.execute(sql, val)
            db.commit()
    cursor.close()
    db.close()
    return
