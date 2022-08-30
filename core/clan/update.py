import sqlite3

from core.clan.getters import get_clan_max_attack, get_clan_min_attack, get_clan_level, get_clan_exp, \
    get_clan_storage, get_clan_guild_boss_hp, get_clan_guild_boss_level


# Clan update

def update_clan_icon(guild_id: int, clan_id: int, icon_url: str) -> None:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    sql = "UPDATE clans SET icon = ? WHERE guild_id = ? AND clan_id = ?"
    values = (icon_url, guild_id, clan_id)
    cursor.execute(sql, values)
    db.commit()
    cursor.close()
    db.close()
    return


def update_clan_min_attack(guild_id: int, clan_id: int, min_attack_to_add: int) -> None:
    min_attack_now = get_clan_min_attack(guild_id, clan_id)
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    sql = "UPDATE clans SET min_attack = ? WHERE guild_id = ? AND clan_id = ?"
    values = (min_attack_now + min_attack_to_add, guild_id, clan_id)
    cursor.execute(sql, values)
    db.commit()
    cursor.close()
    db.close()
    return


def update_clan_max_attack(guild_id: int, clan_id: int, max_attack_to_add: int) -> None:
    max_attack_now = get_clan_max_attack(guild_id, clan_id)
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    sql = "UPDATE clans SET max_attack = ? WHERE guild_id = ? AND clan_id = ?"
    values = (max_attack_now + max_attack_to_add, guild_id, clan_id)
    cursor.execute(sql, values)
    db.commit()
    cursor.close()
    db.close()
    return


def update_clan_level(guild_id: int, clan_id: int, levels_to_add: int) -> None:
    clan_level = get_clan_level(guild_id, clan_id)
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    sql = "UPDATE clans SET clan_level = ? WHERE guild_id = ? AND clan_id = ?"
    values = (clan_level + levels_to_add, guild_id, clan_id)
    cursor.execute(sql, values)
    db.commit()
    cursor.close()
    db.close()
    return


def update_clan_exp(guild_id: int, clan_id: int, exp_to_add: int) -> None:
    clan_exp = get_clan_exp(guild_id, clan_id)
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    sql = "UPDATE clans SET clan_exp = ? WHERE guild_id = ? AND clan_id = ?"
    values = (clan_exp + exp_to_add, guild_id, clan_id)
    cursor.execute(sql, values)
    db.commit()
    cursor.close()
    db.close()
    return


def update_clan_storage(guild_id: int, clan_id: int, money: int) -> None:
    storage = get_clan_storage(guild_id, clan_id)
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    sql = "UPDATE clans SET storage = ? WHERE guild_id = ? AND clan_id = ?"
    values = (storage + money, guild_id, clan_id)
    cursor.execute(sql, values)
    db.commit()
    cursor.close()
    db.close()
    return


def update_clan_description(guild_id: int, clan_id: int, description: str) -> None:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    sql = "UPDATE clans SET clan_description = ? WHERE guild_id = ? AND clan_id = ?"
    values = (description, guild_id, clan_id)
    cursor.execute(sql, values)
    db.commit()
    cursor.close()
    db.close()
    return


def update_clan_boss_level(guild_id: int, clan_id: int, levels_to_update: int) -> None:
    guild_boss_level = get_clan_guild_boss_level(guild_id, clan_id)
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    sql = "UPDATE clans SET guild_boss_level = ? WHERE guild_id = ? AND clan_id = ?"
    values = (guild_boss_level + levels_to_update, guild_id, clan_id)
    cursor.execute(sql, values)
    db.commit()
    cursor.close()
    db.close()
    return


def update_clan_boss_hp(guild_id: int, clan_id: int, hp_to_update: int) -> None:
    guild_boss_hp = get_clan_guild_boss_hp(guild_id, clan_id)
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    sql = "UPDATE clans SET guild_boss_hp = ? WHERE guild_id = ? AND clan_id = ?"
    values = (guild_boss_hp + hp_to_update, guild_id, clan_id)
    cursor.execute(sql, values)
    db.commit()
    cursor.close()
    db.close()
    return


def update_clan_image(guild_id: int, clan_id: int, image: str) -> None:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    sql = "UPDATE clans SET image = ? WHERE guild_id = ? AND clan_id = ?"
    values = (image, guild_id, clan_id)
    cursor.execute(sql, values)
    db.commit()
    cursor.close()
    db.close()
    return


def update_clan_owner_id(guild_id: int, clan_id: int, owner_id: int) -> None:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    sql = "UPDATE clans SET owner_id = ? WHERE guild_id = ? AND clan_id = ?"
    values = (owner_id, guild_id, clan_id)
    cursor.execute(sql, values)
    db.commit()
    cursor.close()
    db.close()
    return


def update_clan_name(guild_id: int, owner_id: int, name: str) -> None:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    sql = "UPDATE clans SET clan_name = ? WHERE guild_id = ? AND owner_id = ?"
    values = (name, guild_id, owner_id)
    cursor.execute(sql, values)
    db.commit()
    cursor.close()
    db.close()
    return


def update_clan_desc_on_creation(guild_id: int, owner_id: int, desc: str) -> None:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    sql = "UPDATE clans SET clan_description = ? WHERE guild_id = ? AND owner_id = ?"
    values = (desc, guild_id, owner_id)
    cursor.execute(sql, values)
    db.commit()
    cursor.close()
    db.close()
    return


def update_clan_color(guild_id: int, owner_id: int, color: str) -> None:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    sql = "UPDATE clans SET clan_color = ? WHERE guild_id = ? AND owner_id = ?"
    values = (color, guild_id, owner_id)
    cursor.execute(sql, values)
    db.commit()
    cursor.close()
    db.close()
    return


def update_clan_icon_on_creation(guild_id: int, owner_id: int, icon: str) -> None:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    sql = "UPDATE clans SET icon = ? WHERE guild_id = ? AND owner_id = ?"
    values = (icon, guild_id, owner_id)
    cursor.execute(sql, values)
    db.commit()
    cursor.close()
    db.close()
    return


def update_user_clan_id(guild_id: int, user_id: int, clan_id: int) -> None:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    sql = "UPDATE clan_members SET clan_id = ? WHERE guild_id = ? AND user_id = ?"
    values = (clan_id, guild_id, user_id)
    cursor.execute(sql, values)
    db.commit()
    cursor.close()
    db.close()
    return


def update_user_join_date(guild_id: int, user_id: int, join_date: str) -> None:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    sql = "UPDATE clan_members SET join_date = ? WHERE guild_id = ? AND user_id = ?"
    values = (join_date, guild_id, user_id)
    cursor.execute(sql, values)
    db.commit()
    cursor.close()
    db.close()
    return


# Config update

def update_server_clan_create_cost(guild_id: int, clan_creation_cost: int) -> None:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    sql = "UPDATE clan_config SET create_cost = ? WHERE guild_id = ?"
    values = (clan_creation_cost, guild_id)
    cursor.execute(sql, values)
    db.commit()
    cursor.close()
    db.close()
    return


def update_server_clan_upgrade_attack_cost(guild_id: int, upgrade_attack_cost: int) -> None:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    sql = "UPDATE clan_config SET upgrade_attack_cost = ? WHERE guild_id = ?"
    values = (upgrade_attack_cost, guild_id)
    cursor.execute(sql, values)
    db.commit()
    cursor.close()
    db.close()
    return


def update_server_clan_upgrade_limit_cost(guild_id: int, upgrade_limit_cost: int) -> None:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    sql = "UPDATE clan_config SET upgrade_limit_cost = ? WHERE guild_id = ?"
    values = (upgrade_limit_cost, guild_id)
    cursor.execute(sql, values)
    db.commit()
    cursor.close()
    db.close()
    return


def update_server_clan_change_icon_cost(guild_id: int, change_icon_cost: int) -> None:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    sql = "UPDATE clan_config SET change_icon_cost = ? WHERE guild_id = ?"
    values = (change_icon_cost, guild_id)
    cursor.execute(sql, values)
    db.commit()
    cursor.close()
    db.close()
    return


def update_server_clan_change_image_cost(guild_id: int, change_image_cost: int) -> None:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    sql = "UPDATE clan_config SET change_icon_cost = ? WHERE guild_id = ?"
    values = (change_image_cost, guild_id)
    cursor.execute(sql, values)
    db.commit()
    cursor.close()
    db.close()
    return


def update_server_clan_upgrade_boss_cost(guild_id: int, upgrade_boss_cost: int) -> None:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    sql = "UPDATE clan_config SET upgrade_boss_cost = ? WHERE guild_id = ?"
    values = (upgrade_boss_cost, guild_id)
    cursor.execute(sql, values)
    db.commit()
    cursor.close()
    db.close()
    return


def update_server_create_clan_channels(guild_id: int, create_clan_channels: bool) -> None:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    sql = "UPDATE clan_config SET create_clan_channels = ? WHERE guild_id = ?"
    values = (create_clan_channels, guild_id)
    cursor.execute(sql, values)
    db.commit()
    cursor.close()
    db.close()
    return


def update_server_clan_voice_category(guild_id: int, create_clan_channels: bool) -> None:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    sql = "UPDATE clan_config SET create_clan_channels = ? WHERE guild_id = ?"
    values = (create_clan_channels, guild_id)
    cursor.execute(sql, values)
    db.commit()
    cursor.close()
    db.close()
    return


def delete_clan(guild_id: int, owner_id: int) -> None:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    sql = "DELETE from clans WHERE guild_id = ? AND owner_id = ?"
    values = (guild_id, owner_id)
    cursor.execute(sql, values)
    db.commit()
    cursor.close()
    db.close()
    return
