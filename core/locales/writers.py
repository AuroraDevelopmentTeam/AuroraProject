from ..db_utils import execute_update
from .getters import LOCALE_CACHE
from core.checkers import is_guild_id_in_table
from config import settings


async def write_in_locales_standart_values(guilds) -> None:
    for guild in guilds:
        if await is_guild_id_in_table("locales", guild.id) is False:
            guild_locale = guild.preferred_locale
            if guild_locale is None:
                guild_locale = settings["default_locale"]
            elif guild_locale == "ru":
                guild_locale = "ru_ru"
            else:
                guild_locale = "en_us"
            sql = "INSERT INTO locales(guild_id, locale) VALUES (%s, %s)"
            val = (guild.id, guild_locale)
            await execute_update(sql, val)
            if guild not in LOCALE_CACHE:
                LOCALE_CACHE[guild] = guild_locale