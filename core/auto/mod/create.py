import sqlite3
from ...db_utils import execute_update

async def create_mod_word_table() -> None:
    await execute_update(
        f"""CREATE TABLE IF NOT EXISTS mod_word (guild_id BIGINT, word TEXT)"""
    )


async def create_mod_config_table() -> None:
    await execute_update(
        f"""CREATE TABLE IF NOT EXISTS mod_config (guild_id BIGINT, word_detect BOOL, link_detect BOOL, 
        nickname_detect BOOL, status_detect BOOL, guild_moderation_mode TEXT) """
    )
