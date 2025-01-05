from ..db_utils import execute_update
from .getters import LOCALE_CACHE


async def update_guild_locale(locale: str, guild_id: int) -> None:
    sql = "UPDATE locales SET locale = %s WHERE guild_id = %s"
    values = (locale, guild_id)
    await execute_update(sql, values)
    LOCALE_CACHE[guild_id] = locale
