import sqlite3
from typing import List, Any

import nextcord


def get_server_autorole_state(guild_id: int) -> bool:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    autoroles_state = cursor.execute(
        f"SELECT autoroles_enabled FROM autoroles WHERE guild_id = {guild_id}"
    ).fetchone()[0]
    cursor.close()
    db.close()
    return bool(autoroles_state)


def get_server_autorole_id(guild_id: int) -> int:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    autorole_id = cursor.execute(
        f"SELECT autorole_id FROM autoroles WHERE guild_id = {guild_id}"
    ).fetchone()[0]
    cursor.close()
    db.close()
    return autorole_id


def get_server_reaction_autorole(guild_id: int, channel_id: int, message_id: int, reaction: str) -> list[int]:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    list_of_autoroles = []
    for row in cursor.execute(
            f"SELECT autorole_id FROM reaction_autorole WHERE guild_id = {guild_id} AND channel_id = {channel_id} AND "
            f"message_id = {message_id} AND reaction = '{reaction}'"
    ):
        list_of_autoroles.append(row[0])
    cursor.close()
    db.close()
    return list_of_autoroles


def check_reaction_autorole(guild_id: int, role: nextcord.Role) -> bool:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    autorole_id = cursor.execute(
        f"SELECT autorole_id FROM reaction_autorole WHERE guild_id = {guild_id} AND autorole_id = {role.id}"
    ).fetchone()
    cursor.close()
    db.close()
    if autorole_id is not None:
        return True
    else:
        return False


def check_level_autorole(guild_id: int, level: int) -> bool:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    autorole_id = cursor.execute(
        f"SELECT autorole_id FROM autoroles_level WHERE guild_id = {guild_id} AND level = {level}"
    ).fetchone()
    cursor.close()
    db.close()
    if autorole_id is not None:
        return True
    else:
        return False


def get_server_level_autorole(guild_id: int, level: int):
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    autorole_id = cursor.execute(
        f"SELECT autorole_id FROM autoroles_level WHERE guild_id = {guild_id} AND level = {level}"
    ).fetchone()[0]
    cursor.close()
    db.close()
    return autorole_id


def list_level_autoroles(guild_id: int):
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    rows = cursor.execute(
        f"SELECT autorole_id, level FROM autoroles_level WHERE guild_id = {guild_id}"
    ).fetchall()
    cursor.close()
    db.close()
    return rows


def list_reaction_autoroles(guild_id: int):
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    rows = cursor.execute(
        f"SELECT autorole_id, reaction FROM reaction_autorole WHERE guild_id = {guild_id}"
    ).fetchall()
    cursor.close()
    db.close()
    return rows
