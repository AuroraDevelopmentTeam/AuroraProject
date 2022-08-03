import sqlite3
from core.checkers import is_guild_id_in_table, is_user_in_table
from config import settings


def write_in_honor_standart_values(guilds) -> None:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    for guild in guilds:
        for member in guild.members:
            if not member.bot:
                if (
                    cursor.execute(
                        f"SELECT user_id FROM honor WHERE user_id = {member.id}"
                    ).fetchone()
                    is None
                ):
                    sql = "INSERT INTO honor(user_id, honor_level, honor_points) VALUES (?, ?, ?)"
                    val = (member.id, 2, 0)
                    cursor.execute(sql, val)
                    db.commit()
    cursor.close()
    db.close()
    return
