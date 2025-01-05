import sqlite3

from ...db_utils import execute_update

async def create_autoroles_table() -> None:
    await execute_update(
        f"""CREATE TABLE IF NOT EXISTS autoroles ( guild_id BIGINT, autoroles_enabled BOOLEAN, 
    autorole_id BIGINT)"""
    )


async def create_level_autorole_table() -> None:
    await execute_update(
        f"""CREATE TABLE IF NOT EXISTS autoroles_level ( guild_id BIGINT, level INTEGER, 
    autorole_id BIGINT)"""
    )


async def create_marriage_autorole_table() -> None:
    await execute_update(
        f"""CREATE TABLE IF NOT EXISTS autoroles_marriage ( guild_id BIGINT, autorole_id BIGINT)"""
    )


async def create_reaction_autorole_table() -> None:
    await execute_update(
        f"""CREATE TABLE IF NOT EXISTS reaction_autorole (guild_id BIGINT, channel_id BIGINT, message_id BIGINT, 
    reaction TEXT, autorole_id BIGINT, is_custom BOOLEAN)"""
    )


async def create_bool_controller() -> None:
    await execute_update(
        f"""CREATE TABLE IF NOT EXISTS autorole_bool (guild_id BIGINT, remove_lvl_roles BOOLEAN)"""
    )
