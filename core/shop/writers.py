import nextcord
import datetime
from core.checkers import is_guild_id_in_table
from core.db_utils import execute_update


async def write_role_in_shop(guild_id: int, role: nextcord.Role, cost: int) -> None:
    sql = "INSERT INTO shop(guild_id, role_id, cost) VALUES (%s, %s, %s)"
    val = (guild_id, role.id, cost)
    await execute_update(sql, val)


async def delete_role_from_shop(guild_id: int, role: nextcord.Role) -> None:
    sql = f"DELETE FROM shop WHERE role_id = {role.id} AND guild_id = {guild_id}"
    await execute_update(sql)


async def write_role_in_custom_shop(
    guild_id: int, role: nextcord.Role, cost: int, owner_id: int
) -> None:
    now = int(datetime.datetime.now().timestamp())
    sql = "INSERT INTO custom_shop(guild_id, role_id, cost, owner_id, created, expiration_date, bought) \
          VALUES (%s, %s, %s, %s, %s, %s, %s)"
    val = (guild_id, role.id, cost, owner_id, now, now + 2592000, 0)
    await execute_update(sql, val)


async def write_in_custom_shop_config_standart_values(
    guilds: list
) -> None:
    for guild in guilds:
        if await is_guild_id_in_table("custom_shop_config", guild.id) is False:
            sql = (
                "INSERT INTO custom_shop_config (guild_id, enabled, role_create_cost) VALUES ("
                "%s, %s) "
            )
            val = (guild.id, True, 0)
            await execute_update(sql, val)
