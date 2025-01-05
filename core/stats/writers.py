from core.checkers import is_guild_id_in_table, is_user_in_table
from core.db_utils import execute_update, fetch_one
from config import settings


async def write_in_stats_standart_values(guilds) -> None:
    for guild in guilds:
        for member in guild.members:
            if not member.bot:
                if await is_user_in_table("stats", guild.id, member.id) is False:
                    sql = "INSERT INTO stats(guild_id, user_id, messages, in_voice, join_time) VALUES (%s, %s, %s, %s, %s)"
                    val = (guild.id, member.id, 0, 0, "0")
                    await execute_update(sql, val)


async def write_channel_in_config(guild_id: int, channel_id: int, enabled: bool) -> None:
    state = await fetch_one(
        f"SELECT enabled FROM stats_channels_config WHERE guild_id = {guild_id} AND channel_id = {channel_id}"
    )
    if state is None:
        sql = "INSERT INTO stats_channels_config(guild_id, channel_id, enabled) VALUES (%s, %s, %s)"
        val = (guild_id, channel_id, enabled)
        await execute_update(sql, val)
    else:
        sql = "UPDATE stats_channels_config SET enabled = %s WHERE guild_id = %s AND channel_id = %s"
        val = (enabled, guild_id, channel_id)
        await execute_update(sql, val)
