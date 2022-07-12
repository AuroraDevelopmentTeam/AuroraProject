import nextcord


def parse_timeouts(guild_members) -> list:
    mutes = []
    counter = 1
    for member in guild_members:
        if member.timeout is not None:
            mutes.append(f"**{counter}**.{member}: **{(member.timeout - nextcord.utils.utcnow()).strftime('%H:%M:%S')}**")
    return mutes
