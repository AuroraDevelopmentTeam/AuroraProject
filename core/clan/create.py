import sqlite3

from ..db_utils import execute_update

async def create_clan_table() -> None:
    await execute_update(
        f"""CREATE TABLE IF NOT EXISTS clans ( guild_id BIGINT, clan_id BIGINT, clan_level INTEGER, clan_exp 
        INTEGER, owner_id BIGINT, member_limit INTEGER, storage INTEGER, create_date TEXT, icon TEXT, image TEXT, 
        min_attack INTEGER, max_attack INTEGER, guild_boss_level INTEGER, guild_boss_hp INTEGER, clan_description 
        TEXT, clan_name TEXT, clan_role BIGINT, clan_voice_channel BIGINT, clan_color TEXT) """
    )


async def create_clan_members_table() -> None:
    await execute_update(
        f"""CREATE TABLE IF NOT EXISTS clan_members (
        guild_id BIGINT, user_id BIGINT, clan_id BIGINT, join_date TEXT
    )"""
    )


async def create_clan_config_table() -> None:
    await execute_update(
        f"""CREATE TABLE IF NOT EXISTS clan_config ( guild_id BIGINT, create_cost INTEGER, upgrade_attack_cost 
        INTEGER, upgrade_limit_cost INTEGER, change_icon_cost INTEGER, change_image_cost INTEGER, 
        upgrade_boss_cost INTEGER, create_clan_channels BOOL, clan_voice_category BIGINT, change_color_cost INTEGER, 
        change_name_cost INTEGER)"""
    )
