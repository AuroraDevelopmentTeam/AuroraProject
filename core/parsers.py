import nextcord
from datetime import datetime


def parse_timeouts(guild_members) -> list:
    mutes = []
    counter = 1
    for member in guild_members:
        if member.timeout is not None:
            estimated_time = member.timeout - nextcord.utils.utcnow()
            estimated_time = f'{estimated_time}'[: -7]
            mutes.append([member.mention, estimated_time])
    return mutes
