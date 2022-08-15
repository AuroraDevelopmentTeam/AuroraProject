import sqlite3
from core.checkers import is_user_in_table


def create_duels_stats_money_table() -> None:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    cursor.execute(
        f"""CREATE TABLE IF NOT EXISTS duels (
        guild_id INTERGER, user_id INTERGER, duels_won INTERGER, games INTERGER, 
        best_attack INTERGER, most_won INTERGER, class TEXT, battle_page TEXT
    )"""
    )
    db.commit()
    cursor.close()
    db.close()
    return


def write_in_duels_standart_values(guilds) -> None:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    for guild in guilds:
        for member in guild.members:
            if not member.bot:
                if is_user_in_table("duels", guild.id, member.id) is False:
                    sql = (
                        "INSERT INTO duels(guild_id, user_id, duels_won, games, "
                        "best_attack, most_won, class, battle_page) "
                        "VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
                    )
                    val = (guild.id, member.id, 0, 0, 0, 0, "rat", "focused_punch")
                    cursor.execute(sql, val)
                    db.commit()
    cursor.close()
    db.close()
    return
