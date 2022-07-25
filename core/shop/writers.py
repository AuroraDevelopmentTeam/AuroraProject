import sqlite3
import nextcord


def write_role_in_shop(guild_id: int, role: nextcord.Role, cost: int) -> None:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    sql = "INSERT INTO shop(guild_id, role_id, cost) VALUES (?, ?, ?)"
    val = (guild_id, role.id, cost)
    cursor.execute(sql, val)
    db.commit()
    cursor.close()
    db.close()


def delete_role_from_shop(guild_id: int, role: nextcord.Role) -> None:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    sql = f"DELETE FROM shop WHERE role_id = {role.id} AND guild_id = {guild_id}"
    cursor.execute(sql)
    db.commit()
    cursor.close()
    db.close()


