import sqlite3
from core.checkers import is_guild_id_in_table


def write_in_tickets_config_standart_values(guilds) -> None:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    for guild in guilds:
        if is_guild_id_in_table("voice_private_config", guild.id) is False:
            sql = (
                "INSERT INTO voice_private_config(guild_id, voice_creation_room_id, voice_controller_msg_id) VALUES ("
                "?, ?, ?) "
            )
            val = (guild.id, 0, 0)
            cursor.execute(sql, val)
            db.commit()
    cursor.close()
    db.close()
    return
