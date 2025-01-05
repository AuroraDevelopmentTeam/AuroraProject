import sqlite3
from core.checkers import is_guild_id_in_table
from config import settings
from core.locales.getters import get_msg_from_locale_by_key

from ...db_utils import execute_update

async def write_in_mod_config_standart_values(guilds) -> None:
    for guild in guilds:
        if await is_guild_id_in_table("mod_config", guild.id) is False:
            sql = (
                "INSERT INTO mod_config(guild_id, word_detect, "
                "link_detect, nickname_detect, status_detect, "
                "guild_moderation_mode) VALUES (%s, %s, %s, %s, %s, %s)"
            )
            val = (guild.id, True, True, True, True, "community")
            await execute_update(sql, val)


async def write_in_mod_word(guild_id: int, word: str) -> None:
    sql = "INSERT INTO mod_word(guild_id, word) VALUES (%s, %s)"
    val = (guild_id, word)
    await execute_update(sql, val)


async def delete_mod_word(guild_id: int, word: str) -> None:
    sql = f"DELETE FROM mod_word WHERE guild_id = {guild_id} AND word = '{word}'"
    val = (guild_id, word)
    await execute_update(sql, val)
