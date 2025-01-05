from core.db_utils import fetch_one


async def get_profile_description(user_id: int) -> str:
    description = await fetch_one(
        f"SELECT description FROM profiles WHERE user_id = {user_id}"
    )
    return description[0]


async def get_avatar_form(user_id: int) -> str:
    avatar_form = await fetch_one(
        f"SELECT avatar_form FROM profiles WHERE user_id = {user_id}"
    )
    return avatar_form[0]
