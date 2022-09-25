import sqlite3
import nextcord


def set_autoroles_state(guild_id: int, autoroles_enabled: bool) -> None:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    sql = "UPDATE autoroles SET autoroles_enabled = ? WHERE guild_id = ?"
    values = (autoroles_enabled, guild_id)
    cursor.execute(sql, values)
    db.commit()
    cursor.close()
    db.close()
    return


def update_autorole(guild_id: int, role_id: int) -> None:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    sql = "UPDATE autoroles SET autorole_id = ? WHERE guild_id = ?"
    values = (role_id, guild_id)
    cursor.execute(sql, values)
    db.commit()
    cursor.close()
    db.close()
    return


def write_autorole_for_level(guild_id: int, role: nextcord.Role, level: int) -> None:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    sql = "INSERT INTO autoroles_level(guild_id, level, autorole_id) VALUES (?, ?, ?)"
    val = (guild_id, level, role.id)
    cursor.execute(sql, val)
    db.commit()
    cursor.close()
    db.close()


def update_autorole_for_level(guild_id: int, role: nextcord.Role, level: int) -> None:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    sql = "UPDATE autoroles_level SET autorole_id = ? WHERE guild_id = ? AND level = ?"
    val = (role.id, guild_id, level)
    cursor.execute(sql, val)
    db.commit()
    cursor.close()
    db.close()


def delete_autorole_for_level(guild_id: int, level: int) -> None:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    sql = f"DELETE FROM autoroles_level WHERE guild_id = {guild_id} AND level = {level}"
    cursor.execute(sql)
    db.commit()
    cursor.close()
    db.close()


def write_autorole_for_reaction(
    guild_id: int,
    channel_id: int,
    message_id: int,
    reaction: str,
    role: nextcord.Role,
    is_custom: bool,
) -> None:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    sql = "INSERT INTO reaction_autorole (guild_id, channel_id, message_id, reaction, autorole_id, is_custom) VALUES " \
          "(?, ?, ?, ?, ?, ?) "
    val = (guild_id, channel_id, message_id, reaction, role.id, is_custom)
    cursor.execute(sql, val)
    db.commit()
    cursor.close()
    db.close()
    return


def delete_autorole_for_reaction(guild_id: int, role: nextcord.Role) -> None:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    sql = f"DELETE FROM reaction_autorole WHERE guild_id = {guild_id} AND autorole_id = {role.id}"
    cursor.execute(sql)
    db.commit()
    cursor.close()
    db.close()
    return


def update_autorole_lvl_deletion_state(guild_id: int, enabled: bool) -> None:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    sql = "UPDATE autorole_bool SET remove_lvl_roles = ? WHERE guild_id = ?"
    val = (enabled, guild_id)
    cursor.execute(sql, val)
    db.commit()
    cursor.close()
    db.close()
    return
