import sqlite3


def create_clan_table() -> None:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    cursor.execute(
        f"""CREATE TABLE IF NOT EXISTS clans ( guild_id INTEGER, clan_id INTEGER, level INTEGER, clan_exp 
        INTEGER, owner_id INTEGER, member_limit INTEGER, storage INTEGER, create_date TEXT, icon TEXT, image TEXT, 
        min_attack INTEGER, max_attack INTEGER, guild_boss_level INTEGER, guild_boss_hp INTEGER, clan_description 
        TEXT, clan_name TEXT ) """
    )
    db.commit()
    cursor.close()
    db.close()
    return


def create_clan_members_table() -> None:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    cursor.execute(
        f"""CREATE TABLE IF NOT EXISTS clan_members (
        guild_id INTEGER, user_id INTEGER, clan_id INTEGER, join_date TEXT
    )"""
    )
    db.commit()
    cursor.close()
    db.close()
    return


def create_clan_config_table() -> None:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    cursor.execute(
        f"""CREATE TABLE IF NOT EXISTS clan_config ( guild_id INTEGER, create_cost INTEGER, upgrade_attack_cost 
        INTEGER, upgrade_limit_cost INTEGER, change_icon_cost INTEGER, upgrade_boss_cost INTEGER) """
    )
    db.commit()
    cursor.close()
    db.close()
    return
