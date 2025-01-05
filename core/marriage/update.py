from ..db_utils import execute_update

from core.locales.getters import get_msg_from_locale_by_key
from core.marriage.getters import (
    get_divorce_counter,
    get_user_gifts_price,
    get_user_gift_counter,
    get_family_money,
    get_user_loveroom_id
)
from core.money.updaters import update_user_balance


async def update_user_pair(guild_id, user_id, pair_id) -> None:
    sql = "UPDATE marriage SET pair_id = %s WHERE guild_id = %s AND user_id = %s"
    values = (pair_id, guild_id, user_id)
    await execute_update(sql, values)


async def update_user_like(guild_id: int, user_id: int, like_id: int) -> None:
    sql = "UPDATE marriage SET like_id = %s WHERE guild_id = %s AND user_id = %s"
    values = (like_id, guild_id, user_id)
    await execute_update(sql, values)


async def update_user_marriage_date(guild_id: int, user_id: int, date) -> None:
    sql = "UPDATE marriage SET date = %s WHERE guild_id = %s AND user_id = %s"
    values = (date, guild_id, user_id)
    await execute_update(sql, values)


async def update_user_loveroom_expire_date(guild_id: int, user_id: int, loveroom_expire_date: int) -> None:
    sql = "UPDATE marriage SET loveroom_expire = %s WHERE guild_id = %s AND user_id = %s"
    values = (loveroom_expire_date, guild_id, user_id)
    await execute_update(sql, values)


async def update_user_loveroom_id(guild_id: int, user_id: int, loveroom_id: int) -> None:
    sql = "UPDATE marriage SET loveroom_id = %s WHERE guild_id = %s AND user_id = %s"
    values = (loveroom_id, guild_id, user_id)
    await execute_update(sql, values)


async def marry_users(guild_id: int, user_id: int, pair_id: int, date):
    default_love_description = get_msg_from_locale_by_key(
        guild_id, "default_love_description"
    )
    await update_user_pair(guild_id, user_id, pair_id)
    await update_user_pair(guild_id, pair_id, user_id)
    await update_user_love_description(guild_id, user_id, default_love_description)
    await update_user_love_description(guild_id, pair_id, default_love_description)
    await update_user_marriage_date(guild_id, user_id, date)
    await update_user_marriage_date(guild_id, pair_id, date)
    await set_couple_family_money(guild_id, user_id, pair_id, 0)


async def divorce_users(guild_id: int, user_id: int, pair_id: int) -> None:
    await update_user_pair(guild_id, user_id, 0)
    await update_user_pair(guild_id, pair_id, 0)
    await increment_user_divorces(guild_id, user_id)
    await increment_user_divorces(guild_id, pair_id)
    await update_user_love_description(guild_id, user_id, "0")
    await update_user_love_description(guild_id, pair_id, "0")
    await update_user_marriage_date(guild_id, user_id, "0")
    await update_user_marriage_date(guild_id, pair_id, "0")
    family_money = await get_family_money(guild_id, user_id)
    await update_user_balance(guild_id, user_id, int(family_money / 2))
    await update_user_balance(guild_id, pair_id, int(family_money / 2))
    await set_couple_family_money(guild_id, user_id, pair_id, 0)
    await update_user_loveroom_expire_date(guild_id, user_id, 0)
    await update_user_loveroom_expire_date(guild_id, pair_id, 0)
    await update_user_loveroom_id(guild_id, user_id, 0)
    await update_user_loveroom_id(guild_id, user_id, 0)


async def increment_user_divorces(guild_id: int, user_id: int) -> None:
    user_divorces = await get_divorce_counter(guild_id, user_id)
    sql = "UPDATE marriage SET divorces = %s WHERE guild_id = %s AND user_id = %s"
    values = (user_divorces + 1, guild_id, user_id)
    await execute_update(sql, values)


async def update_user_love_description(guild_id: int, user_id: int, description: str) -> None:
    sql = "UPDATE marriage SET love_description = %s WHERE guild_id = %s AND user_id = %s"
    values = (description, guild_id, user_id)
    await execute_update(sql, values)


async def update_user_gift_count(guild_id: int, user_id: int, gift: str, amount: int) -> None:
    gift_counter = await get_user_gift_counter(guild_id, user_id, gift)
    sql = f"UPDATE gifts SET {gift} = %s WHERE guild_id = %s AND user_id = %s"
    values = (gift_counter + amount, guild_id, user_id)
    await execute_update(sql, values)


async def set_user_gift_count(guild_id: int, user_id: int, gift: str, amount: int) -> None:
    sql = f"UPDATE gifts SET {gift} = %s WHERE guild_id = %s AND user_id = %s"
    values = (amount, guild_id, user_id)
    await execute_update(sql, values)


async def update_user_gift_price(guild_id: int, user_id: int, price: int) -> None:
    gift_price = await get_user_gifts_price(guild_id, user_id)
    sql = f"UPDATE gifts SET gift_price = %s WHERE guild_id = %s AND user_id = %s"
    values = (gift_price + price, guild_id, user_id)
    await execute_update(sql, values)


async def set_user_gift_price(guild_id: int, user_id: int, price: int) -> None:
    sql = f"UPDATE gifts SET gift_price = %s WHERE guild_id = %s AND user_id = %s"
    values = (price, guild_id, user_id)
    await execute_update(sql, values)


async def set_user_family_money(guild_id: int, user_id: int, amount: int) -> None:
    sql = f"UPDATE marriage SET family_money = %s WHERE guild_id = %s AND user_id = %s"
    values = (amount, guild_id, user_id)
    await execute_update(sql, values)


async def update_user_family_money(guild_id: int, user_id: int, amount: int) -> None:
    family_money = await get_family_money(guild_id, user_id)
    sql = f"UPDATE marriage SET family_money = %s WHERE guild_id = %s AND user_id = %s"
    values = (family_money + amount, guild_id, user_id)
    await execute_update(sql, values)


async def set_couple_family_money(
        guild_id: int, user_id: int, pair_id: int, amount: int
) -> None:
    await set_user_family_money(guild_id, user_id, amount)
    await set_user_family_money(guild_id, pair_id, amount)



async def update_couple_family_money(
        guild_id: int, user_id: int, pair_id: int, amount: int
) -> None:
    await update_user_family_money(guild_id, user_id, amount)
    await update_user_family_money(guild_id, pair_id, amount)


async def update_marriage_config_enable_loverooms(guild_id: int, loveroom_state: bool) -> None:
    sql = f"UPDATE marriage_config SET enable_loverooms = %s WHERE guild_id = %s"
    values = (loveroom_state, guild_id)
    await execute_update(sql, values)


async def update_marriage_config_marriage_price(guild_id: int, marriage_price: int) -> None:
    sql = f"UPDATE marriage_config SET marriage_price = %s WHERE guild_id = %s"
    values = (marriage_price, guild_id)
    await execute_update(sql, values)


async def update_marriage_config_month_loveroom_price(guild_id: int, month_loveroom_price: int) -> None:
    sql = f"UPDATE marriage_config SET month_loveroom_price = %s WHERE guild_id = %s"
    values = (month_loveroom_price, guild_id)
    await execute_update(sql, values)


async def update_marriage_config_loveroom_category(guild_id: int, loveroom_category: int) -> None:
    sql = f"UPDATE marriage_config SET loveroom_category = %s WHERE guild_id = %s"
    values = (loveroom_category, guild_id)
    await execute_update(sql, values)
