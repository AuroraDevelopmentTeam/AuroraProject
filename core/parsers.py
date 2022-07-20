import nextcord
from datetime import datetime
import sqlite3


def parse_timeouts(guild_members) -> list:
    timeouts = []
    for member in guild_members:
        if member.timeout is not None:
            estimated_time = member.timeout - nextcord.utils.utcnow()
            estimated_time = f'{estimated_time}'[: -7]
            timeouts.append([member.mention, estimated_time])
    return timeouts


def parse_warns_of_user(guild_id, user_id) -> list:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    warns = []
    for row in cursor.execute(f"SELECT warn_id, warn_reason FROM warns WHERE guild_id = {guild_id} AND user_id = {user_id}"):
        warn_id = row[0]
        reason = row[1]
        warns.append([warn_id, reason])
    cursor.close()
    db.close()
    return warns
