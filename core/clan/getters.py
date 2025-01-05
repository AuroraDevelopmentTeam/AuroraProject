from core.db_utils import fetch_one, fetch_all

from core.clan.storage import boss_hp, upgrade_price_multipliers


# Clan getters section


async def get_clan_name(guild_id: int, clan_id: int) -> str:
    clan_name = await fetch_one(
        f"SELECT clan_name FROM clans WHERE guild_id = {guild_id} AND clan_id = {clan_id}"
    )
    return clan_name[0]


async def get_clan_description(guild_id: int, clan_id: int) -> str:
    clan_description = await fetch_one(
        f"SELECT clan_description FROM clans WHERE guild_id = {guild_id} AND clan_id = {clan_id}"
    )
    return clan_description[0]


async def get_clan_exp(guild_id: int, clan_id: int) -> int:
    clan_exp = await fetch_one(
        f"SELECT clan_exp FROM clans WHERE guild_id = {guild_id} AND clan_id = {clan_id}"
    )
    return clan_exp[0]


async def get_clan_level(guild_id: int, clan_id: int) -> int:
    clan_level = await fetch_one(
        f"SELECT clan_level FROM clans WHERE guild_id = {guild_id} AND clan_id = {clan_id}"
    )
    return clan_level[0]


async def get_clan_create_date(guild_id: int, clan_id: int) -> str:
    clan_level = await fetch_one(
        f"SELECT create_date FROM clans WHERE guild_id = {guild_id} AND clan_id = {clan_id}"
    )
    return clan_level[0]


async def get_clan_storage(guild_id: int, clan_id: int) -> int:
    clan_storage = await fetch_one(
        f"SELECT storage FROM clans WHERE guild_id = {guild_id} AND clan_id = {clan_id}"
    )
    return clan_storage[0]


async def get_clan_member_limit(guild_id: int, clan_id: int) -> int:
    member_limit = await fetch_one(
        f"SELECT member_limit FROM clans WHERE guild_id = {guild_id} AND clan_id = {clan_id}"
    )
    return member_limit[0]


async def get_clan_icon(guild_id: int, clan_id: int) -> str:
    icon = await fetch_one(
        f"SELECT icon FROM clans WHERE guild_id = {guild_id} AND clan_id = {clan_id}"
    )
    return icon[0]


async def get_clan_image(guild_id: int, clan_id: int) -> str:
    image = await fetch_one(
        f"SELECT image FROM clans WHERE guild_id = {guild_id} AND clan_id = {clan_id}"
    )
    return image[0]


async def get_clan_min_attack(guild_id: int, clan_id: int) -> int:
    image = await fetch_one(
        f"SELECT min_attack FROM clans WHERE guild_id = {guild_id} AND clan_id = {clan_id}"
    )
    return image[0]


async def get_clan_max_attack(guild_id: int, clan_id: int) -> int:
    image = await fetch_one(
        f"SELECT max_attack FROM clans WHERE guild_id = {guild_id} AND clan_id = {clan_id}"
    )
    return image[0]


async def get_clan_guild_boss_level(guild_id: int, clan_id: int) -> int:
    guild_boss_level = await fetch_one(
        f"SELECT guild_boss_level FROM clans WHERE guild_id = {guild_id} AND clan_id = {clan_id}"
    )
    return guild_boss_level[0]


async def get_clan_guild_boss_hp(guild_id: int, clan_id: int) -> int:
    guild_boss_hp = await fetch_one(
        f"SELECT guild_boss_hp FROM clans WHERE guild_id = {guild_id} AND clan_id = {clan_id}"
    )
    return guild_boss_hp[0]


async def get_clan_owner_id(guild_id: int, clan_id: int) -> int:
    owner_id = await fetch_one(
        f"SELECT owner_id FROM clans WHERE guild_id = {guild_id} AND clan_id = {clan_id}"
    )
    return owner_id[0]


async def get_clan_color(guild_id: int, clan_id: int) -> str:
    clan_color = await fetch_one(
        f"SELECT clan_color FROM clans WHERE guild_id = {guild_id} AND clan_id = {clan_id}"
    )
    return clan_color[0]


async def get_clan_role(guild_id: int, clan_id: int) -> int:
    clan_role = await fetch_one(
        f"SELECT clan_role FROM clans WHERE guild_id = {guild_id} AND clan_id = {clan_id}"
    )
    return clan_role[0]


async def get_clan_channel(guild_id: int, clan_id: int) -> int:
    clan_channel = await fetch_one(
        f"SELECT clan_voice_channel FROM clans WHERE guild_id = {guild_id} AND clan_id = {clan_id}"
    )
    return clan_channel[0]


async def get_owner_clan_id(guild_id: int, user_id: int) -> int:
    clan_id = await fetch_one(
        f"SELECT clan_id FROM clans WHERE guild_id = {guild_id} AND owner_id = {user_id}"
    )
    return clan_id[0]


async def get_user_clan_id(guild_id: int, user_id: int) -> int:
    clan_id = await fetch_one(
        f"SELECT clan_id FROM clan_members WHERE guild_id = {guild_id} AND user_id = {user_id}"
    )
    return clan_id[0]


async def get_user_join_date(guild_id: int, user_id: int, clan_id: int) -> int:
    clan_id = await fetch_one(
        f"SELECT join_date FROM clan_members WHERE guild_id = {guild_id} AND user_id = {user_id} AND clan_id = {clan_id}"
    )
    print(clan_id)
    return clan_id[0]


async def fetchall_clan_members(guild_id: int, clan_id: int) -> list:
    clan_members = await fetch_all(
        f"SELECT user_id, join_date FROM clan_members WHERE guild_id = {guild_id} AND clan_id = {clan_id}"
    )
    return clan_members


# __________________________________

# Clan configuration getters section


async def get_server_clan_create_cost(guild_id: int) -> int:
    create_cost = await fetch_one(
        f"SELECT create_cost FROM clan_config WHERE guild_id = {guild_id}"
    )
    return create_cost[0]


async def get_server_clan_change_color_cost(guild_id: int) -> int:
    change_color_cost = await fetch_one(
        f"SELECT change_color_cost FROM clan_config WHERE guild_id = {guild_id}"
    )
    return change_color_cost[0]


async def get_server_clan_upgrade_attack_cost(guild_id: int) -> int:
    upgrade_attack_cost = await fetch_one(
        f"SELECT upgrade_attack_cost FROM clan_config WHERE guild_id = {guild_id}"
    )
    return upgrade_attack_cost[0]


async def get_server_clan_upgrade_limit_cost(guild_id: int) -> int:
    upgrade_limit_cost = await fetch_one(
        f"SELECT upgrade_limit_cost FROM clan_config WHERE guild_id = {guild_id}"
    )
    return upgrade_limit_cost[0]


async def get_server_clan_change_icon_cost(guild_id: int) -> int:
    change_icon_cost = await fetch_one(
        f"SELECT change_icon_cost FROM clan_config WHERE guild_id = {guild_id}"
    )
    return change_icon_cost[0]


async def get_server_clan_change_image_cost(guild_id: int) -> int:
    change_image_cost = await fetch_one(
        f"SELECT change_image_cost FROM clan_config WHERE guild_id = {guild_id}"
    )
    return change_image_cost[0]


async def get_server_clan_upgrade_boss_cost(guild_id: int) -> int:
    upgrade_boss_cost = await fetch_one(
        f"SELECT upgrade_boss_cost FROM clan_config WHERE guild_id = {guild_id}"
    )
    return upgrade_boss_cost[0]


async def get_server_clan_voice_category(guild_id: int) -> int:
    clan_voice_category = await fetch_one(
        f"SELECT clan_voice_category FROM clan_config WHERE guild_id = {guild_id}"
    )
    return clan_voice_category[0]


async def get_server_create_clan_channels(guild_id: int) -> bool:
    create_clan_channels = await fetch_one(
        f"SELECT create_clan_channels FROM clan_config WHERE guild_id = {guild_id}"
    )
    return bool(create_clan_channels[0])


# _____________________________________

# Misc section consisting of all getters integrated together

# _____________________________________


async def get_clan_boss_hp_limit(guild_id: int, clan_id: int):
    boss_level = await get_clan_guild_boss_level(guild_id, clan_id)
    return boss_hp[boss_level]


def get_upgrade_limit_multiplier(limit: int):
    if limit >= 65:
        limit = 65
    return upgrade_price_multipliers["upgrade_limit"][limit]


def get_boss_upgrade_multiplier(boss_level: int):
    return upgrade_price_multipliers["boss_upgrade"][boss_level]
