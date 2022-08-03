import sqlite3
from core.checkers import is_guild_id_in_table, is_user_in_table
from config import settings
from core.locales.getters import get_msg_from_locale_by_key


def write_in_welcomers_config_standart_values(guilds) -> None:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    for guild in guilds:
        if is_guild_id_in_table("welcomers_config", guild.id) is False:
            default_welcome_message_title = get_msg_from_locale_by_key(
                guild.id, "default_welcome_message_title"
            )
            default_welcome_message_description = get_msg_from_locale_by_key(
                guild.id, "default_welcome_message_description"
            )
            default_welcome_message_url = "https://64.media.tumblr.com/ff8de55e7f9f5545c1dec249524cf495/tumblr_nrpg24nMaM1tqou9go2_500.gifv"
            sql = (
                "INSERT INTO welcomers_config(guild_id, welcome_message_enabled, "
                "welcome_message_channel, welcome_message_type, welcome_message_title, "
                "welcome_message_description, welcome_message_url) VALUES (?, ?, ?, ?, ?, ?, ?)"
            )
            val = (
                guild.id,
                settings["default_welcome_messages_state"],
                0,
                settings["default_welcome_messages_type"],
                default_welcome_message_title,
                default_welcome_message_description,
                default_welcome_message_url,
            )
            cursor.execute(sql, val)
            db.commit()
    cursor.close()
    db.close()
    return
