import nextcord
import sqlite3
from core.marriage.getters import GIFT_NAMES, GIFT_EMOJIS, get_user_gift_counter
from core.locales.getters import get_msg_from_locale_by_key
from core.money.getters import get_guild_currency_symbol


def parse_timeouts(guild_members) -> list:
    timeouts = []
    for member in guild_members:
        if member.timeout is not None:
            print(member.timeout)
            try:
                if member.timeout > nextcord.utils.utcnow():
                    estimated_time = member.timeout - nextcord.utils.utcnow()
                    estimated_time = f"{estimated_time}"[:-7]
                    timeouts.append([member.mention, estimated_time])
            except TypeError:
                pass
    return timeouts


def parse_warns_of_user(guild_id, user_id) -> list:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    warns = []
    for row in cursor.execute(
        f"SELECT warn_id, warn_reason FROM warns WHERE guild_id = {guild_id} AND user_id = {user_id}"
    ):
        warn_id = row[0]
        reason = row[1]
        warns.append([warn_id, reason])
    cursor.close()
    db.close()
    return warns


def parse_likes(guild_id, user_id) -> int:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    likes_counter = 0
    for _ in cursor.execute(
        f"SELECT user_id FROM marriage WHERE guild_id = {guild_id} AND like_id = {user_id}"
    ):
        likes_counter += 1
    cursor.close()
    db.close()
    return likes_counter


def parse_user_gifts(guild_id: int, user_id: int) -> str:
    gifts_in_field = 0
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    gifts_description = ""
    for i in range(10):
        gift_now = f"gift_{str(i + 1)}"
        gift_counter = get_user_gift_counter(guild_id, user_id, gift_now)
        if gift_counter > 0:
            gifts_description += f"__**{gift_counter}**__ {GIFT_EMOJIS[gift_now]}⠀⠀"
            gifts_in_field += 1
            if gifts_in_field % 3 == 0:
                gifts_description += "\n"
    cursor.close()
    db.close()
    if len(gifts_description) == 0:
        gifts_description = "-"
    return gifts_description


def parse_server_roles(guild: nextcord.Guild, mention=True) -> list:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    roles = []
    price = get_msg_from_locale_by_key(guild.id, f"price")
    currency_symbol = get_guild_currency_symbol(guild.id)
    counter = 1
    for row in cursor.execute(
        f"SELECT role_id, cost FROM shop WHERE guild_id = {guild.id}"
    ):
        role = guild.get_role(row[0])
        cost = row[1]
        if role is not None:
            if mention is True:
                roles.append(
                    f"**{counter}** • {role.mention}\n{price} **{cost}** {currency_symbol}"
                )
                counter += 1
            else:
                roles.append([role, cost])
    cursor.close()
    db.close()
    return roles
