from core.honor.getters import get_user_honor_level, get_user_honor_points
from ..db_utils import execute_update


async def update_honor_points(user_id: int, honor_points_to_add: int) -> None:
    honor_points_now = await get_user_honor_points(user_id)
    sql = "UPDATE honor SET honor_points = %s WHERE user_id = %s"
    values = (honor_points_now + honor_points_to_add, user_id)
    await execute_update(sql, values)


async def update_honor_level(user_id: int, honor_levels_to_add: int) -> None:
    honor_level = await get_user_honor_level(user_id)
    sql = "UPDATE honor SET honor_level = %s WHERE user_id = %s"
    values = (honor_level + honor_levels_to_add, user_id)
    await execute_update(sql, values)
