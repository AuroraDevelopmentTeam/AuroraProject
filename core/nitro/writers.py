import sqlite3
from core.checkers import is_guild_id_in_table, is_user_in_table
from config import settings
from core.locales.getters import get_msg_from_locale_by_key


def write_in_on_nitro_config_standart_values(guilds) -> None:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    for guild in guilds:
        if is_guild_id_in_table("on_nitro_config", guild.id) is False:
            default_nitro_message_title = get_msg_from_locale_by_key(
                guild.id, "default_nitro_message_title"
            )
            default_nitro_message_description = get_msg_from_locale_by_key(
                guild.id, "default_nitro_message_description"
            )
            default_nitro_message_url = "https://i.imgur.com/MDRkZqC.gif"
            sql = (
                "INSERT INTO on_nitro_config(guild_id, nitro_message_enabled, "
                "nitro_message_channel, nitro_message_title, "
                "nitro_message_description, nitro_message_url) VALUES (?, ?, ?, ?, ?, ?)"
            )
            val = (
                guild.id,
                settings["default_nitro_messages_state"],
                0,
                default_nitro_message_title,
                default_nitro_message_description,
                default_nitro_message_url,
            )
            cursor.execute(sql, val)
            db.commit()
    cursor.close()
    db.close()
    return
