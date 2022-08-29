import sqlite3

from core.clan.getters import get_clan_max_attack, get_clan_min_attack, get_clan_level, get_clan_exp, \
    get_clan_storage, get_clan_guild_boss_hp, get_clan_guild_boss_level


# Changes in clan

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
