from ..db_utils import execute_update
from core.checkers import is_guild_id_in_table, is_user_in_table
from config import settings
from core.locales.getters import get_msg_from_locale_by_key


async def write_in_goodbye_config_standart_values(guilds) -> None:
    for guild in guilds:
        if await is_guild_id_in_table("goodbye_config", guild.id) is False:
            default_goodbye_message_title = get_msg_from_locale_by_key(
                guild.id, "default_goodbye_message_title"
            )
            default_goodbye_message_description = get_msg_from_locale_by_key(
                guild.id, "default_goodbye_message_description"
            )
            default_goodbye_message_url = "https://64.media.tumblr.com/ff8de55e7f9f5545c1dec249524cf495/tumblr_nrpg24nMaM1tqou9go2_500.gifv"
            sql = (
                "INSERT INTO goodbye_config(guild_id, goodbye_message_enabled, "
                "goodbye_message_channel, goodbye_message_type, goodbye_message_title, "
                "goodbye_message_description, goodbye_message_url) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            )
            val = (
                guild.id,
                settings["default_goodbye_messages_state"],
                0,
                settings["default_goodbye_messages_type"],
                default_goodbye_message_title,
                default_goodbye_message_description,
                default_goodbye_message_url,
            )
            await execute_update(sql, val)
    return
