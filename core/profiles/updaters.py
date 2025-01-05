from core.db_utils import execute_update


async def update_profile_description(user_id: int, description: str) -> None:
    sql = "UPDATE profiles SET description = %s WHERE user_id = %s"
    values = (description, user_id)
    await execute_update(sql, values)


async def update_avatar_form(user_id: int, avatar_form: str) -> None:
    sql = "UPDATE profiles SET avatar_form = %s WHERE user_id = %s"
    values = (avatar_form, user_id)
    await execute_update(sql, values)
