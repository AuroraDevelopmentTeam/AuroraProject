import sqlite3

from core.checkers import is_user_in_table


def write_in_marriage_standart_values(guilds) -> None:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    for guild in guilds:
        for member in guild.members:
            if not member.bot:
                if is_user_in_table("marriage", guild.id, member.id) is False:
                    sql = (
                        "INSERT INTO marriage(guild_id, user_id, pair_id, like_id, divorces, love_description, "
                        "date, family_money, loveroom_expire) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
                    )
                    val = (guild.id, member.id, 0, 0, 0, "0", "0", 0, 0)
                    cursor.execute(sql, val)
                    db.commit()
    cursor.close()
    db.close()
    return


def write_in_marriage_config_standart_values(guilds) -> None:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    for guild in guilds:
        for member in guild.members:
            if not member.bot:
                if is_user_in_table("marriage_config", guild.id, member.id) is False:
                    sql = (
                        "INSERT INTO marriage_config(guild_id, enable_loverooms, marriage_price, "
                        "month_loveroom_price) VALUES (?, ?, ?, ?) "
                    )
                    val = (guild.id, member.id, 0, 0, 0, "0", "0", 0, 0)
                    cursor.execute(sql, val)
                    db.commit()
    cursor.close()
    db.close()
    return


def write_in_gifts_standart_values(guilds) -> None:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    for guild in guilds:
        for member in guild.members:
            if not member.bot:
                if is_user_in_table("gifts", guild.id, member.id) is False:
                    sql = (
                        "INSERT INTO gifts(guild_id, user_id, gift_1, gift_2, gift_3, gift_4, gift_5, gift_6, "
                        "gift_7, gift_8, gift_9, gift_10, gift_price) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
                    )
                    val = (guild.id, member.id, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
                    cursor.execute(sql, val)
                    db.commit()
    cursor.close()
    db.close()
    return
