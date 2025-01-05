from core.db_utils import fetch_one


async def check_warn(guild_id, warn_id):
    if (
        await fetch_one(
            f"SELECT warn_id FROM warns WHERE guild_id = {guild_id} AND warn_id = {warn_id}"
        )
        is None
    ):
        return False
    return True


async def get_warn_reason(guild_id: int, user_id: int) -> str:
    warn_reason = await fetch_one(
        f"SELECT warn_reason FROM warns WHERE guild_id = {guild_id} AND user_id = {user_id}"
    )
    return warn_reason[0]
