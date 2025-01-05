from core.db_utils import execute_update, fetch_one
from core.checkers import is_guild_id_in_table, is_user_in_table
from core.locales.getters import get_msg_from_locale_by_key
from config import settings


async def write_in_profiles_standart_values(guilds) -> None:
    for guild in guilds:
        description = get_msg_from_locale_by_key(
            guild.id, "default_profile_description"
        )
        for member in guild.members:
            if not member.bot:
                if (
                    await fetch_one(
                        f"SELECT user_id FROM profiles WHERE user_id = {member.id}"
                    )
                    is None
                ):
                    sql = "INSERT INTO profiles(user_id, description, avatar_form) VALUES (%s, %s, %s)"
                    val = (
                        member.id,
                        description,
                        settings["default_profile_avatar_form"],
                    )
                    await execute_update(sql, val)
