from core.db_utils import fetch_one
import nextcord

from core.marriage.getters import get_user_pair_id


async def is_guild_id_in_table(table_name: str, guild_id: int) -> bool:
    if (
        await fetch_one(
            f"SELECT guild_id FROM {table_name} WHERE guild_id = {guild_id}"
        )
        is None
    ):
        return False
    return True


async def is_warn_id_in_table(
    table_name: str, warn_id: int, guild_id: int, user_id: int
) -> bool:
    if (
        await fetch_one(
            f"SELECT warn_id FROM {table_name} WHERE warn_id = {warn_id} "
            f"AND guild_id = {guild_id} AND user_id = {user_id}"
        )
        is None
    ):
        return False
    return True


def is_locale_valid(locale: str) -> bool:
    locales = ["en_us", "ru_ru"]
    if locale in locales:
        return True
    else:
        return False


async def is_user_in_table(table_name, guild_id, user_id) -> bool:
    if (
        await fetch_one(
            f"SELECT user_id FROM {table_name} WHERE guild_id = {guild_id} "
            f"AND user_id = {user_id}"
        )
        is None
    ):
        return False
    return True


def is_str_or_emoji(symbol) -> bool:
    if isinstance(symbol, str) or isinstance(symbol, nextcord.Emoji):
        return True
    else:
        return False


async def is_married(guild_id, user_id) -> bool:
    # pair_id = await get_user_pair_id(guild_id, user_id)
    # if pair_id == 0:
    #     return False
    # return True
    return await get_user_pair_id(guild_id, user_id) != 0

async def is_role_in_shop(guild_id, role_id) -> bool:
    if (
        await fetch_one(
            f"SELECT role_id FROM shop WHERE guild_id = {guild_id} "
            f"AND role_id = {role_id}"
        )
        is None
    ):
        return False
    return True


async def is_role_in_income(guild_id, role_id) -> bool:
    if (
        await fetch_one(
            f"SELECT role_id FROM roles_money WHERE guild_id = {guild_id} "
            f"AND role_id = {role_id}"
        )
        is None
    ):
        return False
    return True


async def is_channel_in_config(guild_id, channel_id) -> bool:
    if (
        await fetch_one(
            f"SELECT channel_id FROM money_channels_config WHERE guild_id = {guild_id} "
            f"AND channel_id = {channel_id}"
        )
        is None
    ):
        return False
    return True
