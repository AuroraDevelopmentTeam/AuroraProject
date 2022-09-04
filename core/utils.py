import sqlite3
import typing
from typing import Type, Any

from config import settings

import nextcord
from core.checkers import is_user_in_table
from core.locales.getters import get_msg_from_locale_by_key


def format_seconds_to_hhmmss(seconds):
    hours = seconds // (60 * 60)
    seconds %= 60 * 60
    minutes = seconds // 60
    seconds %= 60
    return "%02i:%02i:%02i" % (hours, minutes, seconds)


def write_member_in_money(guild: nextcord.Guild, member: nextcord.Member):
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    guild_starting_balance = cursor.execute(
        f"SELECT guild_starting_balance FROM money_config WHERE guild_id = {guild.id}"
    ).fetchone()[0]
    if not member.bot:
        if is_user_in_table("money", guild.id, member.id) is False:
            sql = "INSERT INTO money(guild_id, user_id, balance) VALUES (?, ?, ?)"
            val = (guild.id, member.id, guild_starting_balance)
            cursor.execute(sql, val)
            db.commit()
    cursor.close()
    db.close()
    return


def write_member_in_levels(guild: nextcord.Guild, member: nextcord.Member) -> None:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    if not member.bot:
        if is_user_in_table("levels", guild.id, member.id) is False:
            sql = (
                "INSERT INTO levels(guild_id, user_id, level, exp) VALUES (?, ?, ?, ?)"
            )
            val = (guild.id, member.id, 1, 0)
            cursor.execute(sql, val)
            db.commit()
    cursor.close()
    db.close()
    return


def write_member_in_marriage(guild: nextcord.Guild, member: nextcord.Member) -> None:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    if not member.bot:
        if is_user_in_table("marriage", guild.id, member.id) is False:
            sql = (
                "INSERT INTO marriage(guild_id, user_id, pair_id, like_id, divorces, love_description, "
                "date, family_money) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
            )
            val = (guild.id, member.id, 0, 0, 0, "0", "0", 0)
            cursor.execute(sql, val)
            db.commit()
    cursor.close()
    db.close()
    return


def write_member_in_gifts(guild: nextcord.Guild, member: nextcord.Member) -> None:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
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


def write_member_in_honor(member: nextcord.Member) -> None:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    if not member.bot:
        if (
                cursor.execute(
                    f"SELECT user_id FROM honor WHERE user_id = {member.id}"
                ).fetchone()
                is None
        ):
            sql = (
                "INSERT INTO honor(user_id, honor_level, honor_points) VALUES (?, ?, ?)"
            )
            val = (member.id, 2, 0)
            cursor.execute(sql, val)
            db.commit()
    cursor.close()
    db.close()


def write_member_in_profiles(guild: nextcord.Guild, member: nextcord.Member) -> None:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    description = get_msg_from_locale_by_key(guild.id, "default_profile_description")
    if not member.bot:
        if (
                cursor.execute(
                    f"SELECT user_id FROM profiles WHERE user_id = {member.id}"
                ).fetchone()
                is None
        ):
            sql = "INSERT INTO profiles(user_id, description, avatar_form) VALUES (?, ?, ?)"
            val = (
                member.id,
                description,
                settings["default_profile_avatar_form"],
            )
            cursor.execute(sql, val)
            db.commit()
    cursor.close()
    db.close()
    return


def write_member_in_stats(guild: nextcord.Guild, member: nextcord.Member) -> None:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    if not member.bot:
        if is_user_in_table("stats", guild.id, member.id) is False:
            sql = "INSERT INTO stats(guild_id, user_id, messages, in_voice, join_time) VALUES (?, ?, ?, ?, ?)"
            val = (guild.id, member.id, 0, 0, "0")
            cursor.execute(sql, val)
            db.commit()
    cursor.close()
    db.close()
    return


def write_member_in_badges(guild: nextcord.Guild, member: nextcord.Member) -> None:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    if not member.bot:
        if is_user_in_table("badges", guild.id, member.id) is False:
            sql = (
                "INSERT INTO badges(guild_id, user_id, badge_1, badge_2, badge_3, badge_4, badge_5, badge_6, "
                "badge_7, badge_8, badge_9) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
            )
            val = (
                guild.id,
                member.id,
                False,
                False,
                False,
                False,
                False,
                False,
                False,
                False,
                False,
            )
            cursor.execute(sql, val)
            db.commit()
    cursor.close()
    db.close()
    return


class PlatformType:
    def __init__(self):
        pass


class MobilePlatform(PlatformType):
    def __init__(self):
        super().__init__()


class DesktopPlatform(PlatformType):
    def __init__(self):
        super().__init__()


def parse_status_to_int(status: nextcord.Status) -> int:
    status_parse_to_int = {
        nextcord.Status.offline: 0,
        nextcord.Status.invisible: 0,
        nextcord.Status.dnd: 1,
        nextcord.Status.do_not_disturb: 1,
        nextcord.Status.idle: 2,
        nextcord.Status.online: 3,
    }
    return status_parse_to_int[status]


def calculate_platform_type(user: typing.Union[nextcord.User, nextcord.Member]) -> Type[PlatformType]:
    desktop_status = parse_status_to_int(user.desktop_status)
    browser_status = parse_status_to_int(user.web_status)
    mobile_status = parse_status_to_int(user.mobile_status)
    if mobile_status >= desktop_status or mobile_status >= browser_status + desktop_status:
        return MobilePlatform
    else:
        return DesktopPlatform
