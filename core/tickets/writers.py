import sqlite3
from core.checkers import is_guild_id_in_table, is_user_in_table


def write_in_tickets_config_standart_values(guilds) -> None:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    for guild in guilds:
        if is_guild_id_in_table("tickets_config", guild.id) is False:
            sql = (
                "INSERT INTO tickets_config(guild_id, ticket_category, "
                "ticket_archive, ticket_support) VALUES (?, ?, ?, ?)"
            )
            val = (guild.id, 0, 0, 0)
            cursor.execute(sql, val)
            db.commit()
    cursor.close()
    db.close()
    return
