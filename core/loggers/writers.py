from ..db_utils import execute_update
from core.checkers import is_guild_id_in_table, is_user_in_table
from config import settings
from core.locales.getters import get_msg_from_locale_by_key


async def write_in_loggers_standart_values(guilds) -> None:
    for guild in guilds:
        if await is_guild_id_in_table("loggers", guild.id) is False:
            sql = (
                "INSERT INTO loggers(guild_id, log_channel_id, "
                "logs_enabled) VALUES (%s, %s, %s)"
            )
            val = (guild.id, 0, settings["default_logs_enabled"])
            await execute_update(sql, val)
