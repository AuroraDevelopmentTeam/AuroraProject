import sqlite3
from core.checkers import is_guild_id_in_table, is_user_in_table


def write_in_autoroles_standart_values(guilds) -> None:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    for guild in guilds:
        if is_guild_id_in_table("autoroles", guild.id) is False:
            sql = (
                "INSERT INTO autoroles(guild_id, autoroles_enabled, "
                "autorole_id) VALUES (?, ?, ?)"
            )
            val = (guild.id, True, 0)
            cursor.execute(sql, val)
            db.commit()
    cursor.close()
    db.close()
    return


def write_in_levelroles_value(guild_id, level, role_id):
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    sql = "INSERT INTO autoroles_level(guild_id, level, autorole_id) VALUES (?, ?, ?)"
    val = (guild_id, level, role_id)
    cursor.execute(sql, val)
    db.commit()
    cursor.close()
    db.close()
    return


def write_in_autoroles_bool_standart_values(guilds) -> None:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    for guild in guilds:
        if is_guild_id_in_table("autorole_bool", guild.id) is False:
            sql = (
                "INSERT INTO autorole_bool(guild_id, remove_lvl_roles) VALUES (?, ?)"
            )
            val = (guild.id, False)
            cursor.execute(sql, val)
            db.commit()
    cursor.close()
    db.close()
    return
