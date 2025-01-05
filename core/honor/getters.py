from ..db_utils import fetch_one


async def get_user_honor_points(user_id: int) -> int:
    honor_points = await fetch_one(
        f"SELECT honor_points FROM honor WHERE user_id = {user_id}"
    )
    return honor_points[0]


async def get_user_honor_level(user_id: int) -> int:
    honor_level = await fetch_one(
        f"SELECT honor_level FROM honor WHERE user_id = {user_id}"
    )
    return honor_level[0]


def get_rome_symbol(number: int) -> str:
    if number > 5:
        number = 5
    rome_number = {1: "I", 2: "II", 3: "III", 4: "IV", 5: "V"}
    return rome_number[number]
