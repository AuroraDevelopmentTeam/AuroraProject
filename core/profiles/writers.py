import sqlite3
from core.checkers import is_guild_id_in_table, is_user_in_table
from core.locales.getters import get_msg_from_locale_by_key
from config import settings


def write_in_profiles_standart_values(guilds) -> None:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    for guild in guilds:
        description = get_msg_from_locale_by_key(guild.id, "default_profile_description")
        for member in guild.members:
            if not member.bot:
                if cursor.execute(f"SELECT user_id FROM profiles WHERE user_id = {member.id}").fetchone() is None:
                    sql = "INSERT INTO profiles(user_id, description, avatar_form) VALUES (?, ?, ?)"
                    val = (member.id, description, settings['default_profile_avatar_form'])
                    cursor.execute(sql, val)
                    db.commit()
    cursor.close()
    db.close()
    return
