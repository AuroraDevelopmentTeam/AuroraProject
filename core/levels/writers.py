import sqlite3
from core.checkers import is_guild_id_in_table, is_user_in_table
from config import settings


def write_in_levels_config_standart_values(guilds) -> None:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    for guild in guilds:
        if is_guild_id_in_table("levels_config", guild.id) is False:
            sql = (
                "INSERT INTO levels_config(guild_id, min_exp_per_message, max_exp_per_message, "
                "level_up_messages_state) VALUES (?, ?, ?, ?)"
            )
            val = (
                guild.id,
                settings["default_min_exp"],
                settings["default_max_exp"],
                settings["default_level_up_messages_state"],
            )
            cursor.execute(sql, val)
            db.commit()
    cursor.close()
    db.close()
    return


def write_in_levels_standart_values(guilds) -> None:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    for guild in guilds:
        for member in guild.members:
            if not member.bot:
                if is_user_in_table("levels", guild.id, member.id) is False:
                    sql = "INSERT INTO levels(guild_id, user_id, level, exp) VALUES (?, ?, ?, ?)"
                    val = (guild.id, member.id, 1, 0)
                    cursor.execute(sql, val)
                    db.commit()
    cursor.close()
    db.close()
    return


def write_channel_in_config(guild_id: int, channel_id: int, enabled: bool) -> None:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    sql = "INSERT INTO level_channels_config(guild_id, channel_id, enabled) VALUES (?, ?, ?)"
    val = (guild_id, channel_id, enabled)
    cursor.execute(sql, val)
    db.commit()
    cursor.close()
    db.close()
