import sqlite3

import nextcord

from ...db_utils import fetch_one, fetch_all

async def get_server_word_detect(guild_id: int) -> bool:
    word_detect = await fetch_one(
        f"SELECT word_detect FROM mod_config WHERE guild_id = {guild_id}"
    )
    return bool(word_detect[0])


async def get_server_link_detect(guild_id: int) -> bool:
    link_detect = await fetch_one(
        f"SELECT link_detect FROM mod_config WHERE guild_id = {guild_id}"
    )
    return bool(link_detect[0])


async def get_server_nickname_detect(guild_id: int) -> bool:
    nickname_detect = await fetch_one(
        f"SELECT nickname_detect FROM mod_config WHERE guild_id = {guild_id}"
    )
    return bool(nickname_detect[0])


async def get_server_status_detect(guild_id: int) -> bool:
    status_detect = fetch_one(
        f"SELECT status_detect FROM mod_config WHERE guild_id = {guild_id}"
    )
    return bool(status_detect[0])


async def get_server_moderation_mode(guild_id: int) -> str:
    guild_moderation_mode = await fetch_one(
        f"SELECT guild_moderation_mode FROM mod_config WHERE guild_id = {guild_id}"
    )
    return guild_moderation_mode[0]


async def fetchall_mod_words(guild_id: int) -> list[str]:
    mod_words = await fetch_all(
        f"SELECT word FROM mod_word WHERE guild_id = {guild_id}"
    )
    words = []
    for row in mod_words:
        words.append(row[0])
    return words
