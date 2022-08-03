import sqlite3

from core.checkers import is_guild_id_in_table, is_user_in_table
from config import settings


def write_in_stats_standart_values(guilds) -> None:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    for guild in guilds:
        for member in guild.members:
            if not member.bot:
                if is_user_in_table("stats", guild.id, member.id) is False:
                    sql = "INSERT INTO stats(guild_id, user_id, messages, in_voice, join_time) VALUES (?, ?, ?, ?, ?)"
                    val = (guild.id, member.id, 0, 0, "0")
                    cursor.execute(sql, val)
                    db.commit()
    cursor.close()
    db.close()
    return
