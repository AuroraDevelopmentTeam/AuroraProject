from ..db_utils import execute_update

from core.checkers import is_user_in_table, is_guild_id_in_table


async def write_in_marriage_standart_values(guilds) -> None:
    for guild in guilds:
        for member in guild.members:
            if not member.bot:
                if await is_user_in_table("marriage", guild.id, member.id) is False:
                    sql = (
                        "INSERT INTO marriage(guild_id, user_id, pair_id, like_id, divorces, love_description, "
                        "date, family_money, loveroom_expire, loveroom_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                    )
                    val = (guild.id, member.id, 0, 0, 0, "0", "0", 0, 0, 0)
                    await execute_update(sql, val)


async def write_in_marriage_config_standart_values(guilds) -> None:
    for guild in guilds:
        if await is_guild_id_in_table("marriage_config", guild.id) is False:
            sql = (
                "INSERT INTO marriage_config(guild_id, enable_loverooms, marriage_price, "
                "month_loveroom_price, loveroom_category) VALUES (%s, %s, %s, %s, %s) "
            )
            val = (guild.id, True, 10000, 40000, 0)
            await execute_update(sql, val)


async def write_in_gifts_standart_values(guilds) -> None:
    for guild in guilds:
        for member in guild.members:
            if not member.bot:
                if await is_user_in_table("gifts", guild.id, member.id) is False:
                    sql = (
                        "INSERT INTO gifts(guild_id, user_id, gift_1, gift_2, gift_3, gift_4, gift_5, gift_6, "
                        "gift_7, gift_8, gift_9, gift_10, gift_price) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                    )
                    val = (guild.id, member.id, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
                    await execute_update(sql, val)


async def write_new_column(guilds) -> None:

    query = "ALTER TABLE marriage ADD loveroom_id BIGINT"

    await execute_update(query)

    for guild in guilds:
        for member in guild.members:
            if not member.bot:
                if await is_user_in_table("marriage", guild.id, member.id) is True:
                    sql = (
                        "INSERT INTO marriage(loveroom_id) VALUES (%s)"
                    )
                    val = ["0"]
                    await execute_update(sql, val)
