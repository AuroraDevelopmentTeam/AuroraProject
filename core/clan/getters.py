import sqlite3

from core.clan.storage import boss_hp, upgrade_price_multipliers


# Clan getters section


def get_clan_name(guild_id: int, clan_id: int) -> str:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    clan_name = cursor.execute(
        f"SELECT clan_name FROM clans WHERE guild_id = {guild_id} AND clan_id = {clan_id}"
    ).fetchone()[0]
    cursor.close()
    db.close()
    return clan_name


def get_clan_description(guild_id: int, clan_id: int) -> str:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    clan_description = cursor.execute(
        f"SELECT clan_description FROM clans WHERE guild_id = {guild_id} AND clan_id = {clan_id}"
    ).fetchone()[0]
    cursor.close()
    db.close()
    return clan_description


def get_clan_exp(guild_id: int, clan_id: int) -> int:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    clan_exp = cursor.execute(
        f"SELECT clan_exp FROM clans WHERE guild_id = {guild_id} AND clan_id = {clan_id}"
    ).fetchone()[0]
    cursor.close()
    db.close()
    return clan_exp


def get_clan_level(guild_id: int, clan_id: int) -> int:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    clan_level = cursor.execute(
        f"SELECT clan_level FROM clans WHERE guild_id = {guild_id} AND clan_id = {clan_id}"
    ).fetchone()[0]
    cursor.close()
    db.close()
    return clan_level


def get_clan_create_date(guild_id: int, clan_id: int) -> str:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    clan_level = cursor.execute(
        f"SELECT create_date FROM clans WHERE guild_id = {guild_id} AND clan_id = {clan_id}"
    ).fetchone()[0]
    cursor.close()
    db.close()
    return clan_level


def get_clan_storage(guild_id: int, clan_id: int) -> int:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    clan_storage = cursor.execute(
        f"SELECT storage FROM clans WHERE guild_id = {guild_id} AND clan_id = {clan_id}"
    ).fetchone()[0]
    cursor.close()
    db.close()
    return clan_storage


def get_clan_member_limit(guild_id: int, clan_id: int) -> int:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    member_limit = cursor.execute(
        f"SELECT member_limit FROM clans WHERE guild_id = {guild_id} AND clan_id = {clan_id}"
    ).fetchone()[0]
    cursor.close()
    db.close()
    return member_limit


def get_clan_icon(guild_id: int, clan_id: int) -> str:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    icon = cursor.execute(
        f"SELECT icon FROM clans WHERE guild_id = {guild_id} AND clan_id = {clan_id}"
    ).fetchone()[0]
    cursor.close()
    db.close()
    return icon


def get_clan_image(guild_id: int, clan_id: int) -> str:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    image = cursor.execute(
        f"SELECT image FROM clans WHERE guild_id = {guild_id} AND clan_id = {clan_id}"
    ).fetchone()[0]
    cursor.close()
    db.close()
    return image


def get_clan_min_attack(guild_id: int, clan_id: int) -> int:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    image = cursor.execute(
        f"SELECT min_attack FROM clans WHERE guild_id = {guild_id} AND clan_id = {clan_id}"
    ).fetchone()[0]
    cursor.close()
    db.close()
    return image


def get_clan_max_attack(guild_id: int, clan_id: int) -> int:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    image = cursor.execute(
        f"SELECT max_attack FROM clans WHERE guild_id = {guild_id} AND clan_id = {clan_id}"
    ).fetchone()[0]
    cursor.close()
    db.close()
    return image


def get_clan_guild_boss_level(guild_id: int, clan_id: int) -> int:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    guild_boss_level = cursor.execute(
        f"SELECT guild_boss_level FROM clans WHERE guild_id = {guild_id} AND clan_id = {clan_id}"
    ).fetchone()[0]
    cursor.close()
    db.close()
    return guild_boss_level


def get_clan_guild_boss_hp(guild_id: int, clan_id: int) -> int:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    guild_boss_hp = cursor.execute(
        f"SELECT guild_boss_hp FROM clans WHERE guild_id = {guild_id} AND clan_id = {clan_id}"
    ).fetchone()[0]
    cursor.close()
    db.close()
    return guild_boss_hp


def get_clan_owner_id(guild_id: int, clan_id: int) -> int:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    owner_id = cursor.execute(
        f"SELECT owner_id FROM clans WHERE guild_id = {guild_id} AND clan_id = {clan_id}"
    ).fetchone()[0]
    cursor.close()
    db.close()
    return owner_id


def get_clan_color(guild_id: int, clan_id: int) -> str:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    clan_color = cursor.execute(
        f"SELECT clan_color FROM clans WHERE guild_id = {guild_id} AND clan_id = {clan_id}"
    ).fetchone()[0]
    cursor.close()
    db.close()
    return clan_color


def get_clan_role(guild_id: int, clan_id: int) -> int:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    clan_role = cursor.execute(
        f"SELECT clan_role FROM clans WHERE guild_id = {guild_id} AND clan_id = {clan_id}"
    ).fetchone()[0]
    cursor.close()
    db.close()
    return clan_role


def get_clan_channel(guild_id: int, clan_id: int) -> int:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    clan_channel = cursor.execute(
        f"SELECT clan_voice_channel FROM clans WHERE guild_id = {guild_id} AND clan_id = {clan_id}"
    ).fetchone()[0]
    cursor.close()
    db.close()
    return clan_channel


def get_owner_clan_id(guild_id: int, user_id: int) -> int:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    clan_id = cursor.execute(
        f"SELECT clan_id FROM clans WHERE guild_id = {guild_id} AND owner_id = {user_id}"
    ).fetchone()[0]
    cursor.close()
    db.close()
    return clan_id


def get_user_clan_id(guild_id: int, user_id: int) -> int:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    clan_id = cursor.execute(
        f"SELECT clan_id FROM clan_members WHERE guild_id = {guild_id} AND user_id = {user_id}"
    ).fetchone()[0]
    cursor.close()
    db.close()
    return clan_id


def get_user_join_date(guild_id: int, user_id: int, clan_id: int) -> int:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    clan_id = cursor.execute(
        f"SELECT join_date FROM clan_members WHERE guild_id = {guild_id} AND user_id = {user_id} AND clan_id = {clan_id}"
    ).fetchone()[0]
    cursor.close()
    db.close()
    return clan_id


def fetchall_clan_members(guild_id: int, clan_id: int) -> list:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    clan_members = cursor.execute(
        f"SELECT user_id, join_date FROM clan_members WHERE guild_id = {guild_id} AND clan_id = {clan_id}"
    ).fetchall()
    cursor.close()
    db.close()
    return clan_members


# __________________________________

# Clan configuration getters section


def get_server_clan_create_cost(guild_id: int) -> int:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    create_cost = cursor.execute(
        f"SELECT create_cost FROM clan_config WHERE guild_id = {guild_id}"
    ).fetchone()[0]
    cursor.close()
    db.close()
    return create_cost


def get_server_clan_change_color_cost(guild_id: int) -> int:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    change_color_cost = cursor.execute(
        f"SELECT change_color_cost FROM clan_config WHERE guild_id = {guild_id}"
    ).fetchone()[0]
    cursor.close()
    db.close()
    return change_color_cost


def get_server_clan_upgrade_attack_cost(guild_id: int) -> int:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    upgrade_attack_cost = cursor.execute(
        f"SELECT upgrade_attack_cost FROM clan_config WHERE guild_id = {guild_id}"
    ).fetchone()[0]
    cursor.close()
    db.close()
    return upgrade_attack_cost


def get_server_clan_upgrade_limit_cost(guild_id: int) -> int:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    upgrade_limit_cost = cursor.execute(
        f"SELECT upgrade_limit_cost FROM clan_config WHERE guild_id = {guild_id}"
    ).fetchone()[0]
    cursor.close()
    db.close()
    return upgrade_limit_cost


def get_server_clan_change_icon_cost(guild_id: int) -> int:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    change_icon_cost = cursor.execute(
        f"SELECT change_icon_cost FROM clan_config WHERE guild_id = {guild_id}"
    ).fetchone()[0]
    cursor.close()
    db.close()
    return change_icon_cost


def get_server_clan_change_image_cost(guild_id: int) -> int:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    change_image_cost = cursor.execute(
        f"SELECT change_image_cost FROM clan_config WHERE guild_id = {guild_id}"
    ).fetchone()[0]
    cursor.close()
    db.close()
    return change_image_cost


def get_server_clan_upgrade_boss_cost(guild_id: int) -> int:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    upgrade_boss_cost = cursor.execute(
        f"SELECT upgrade_boss_cost FROM clan_config WHERE guild_id = {guild_id}"
    ).fetchone()[0]
    cursor.close()
    db.close()
    return upgrade_boss_cost


def get_server_clan_voice_category(guild_id: int) -> int:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    clan_voice_category = cursor.execute(
        f"SELECT clan_voice_category FROM clan_config WHERE guild_id = {guild_id}"
    ).fetchone()[0]
    cursor.close()
    db.close()
    return clan_voice_category


def get_server_create_clan_channels(guild_id: int) -> bool:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    create_clan_channels = cursor.execute(
        f"SELECT create_clan_channels FROM clan_config WHERE guild_id = {guild_id}"
    ).fetchone()[0]
    cursor.close()
    db.close()
    return bool(create_clan_channels)


# _____________________________________

# Misc section consisting of all getters integrated together

# _____________________________________


def get_clan_boss_hp_limit(guild_id: int, clan_id: int):
    boss_level = get_clan_guild_boss_level(guild_id, clan_id)
    return boss_hp[boss_level]


def get_upgrade_limit_multiplier(limit: int):
    if limit >= 65:
        limit = 65
    return upgrade_price_multipliers["upgrade_limit"][limit]


def get_boss_upgrade_multiplier(boss_level: int):
    return upgrade_price_multipliers["boss_upgrade"][boss_level]
