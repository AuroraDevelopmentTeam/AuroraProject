import datetime
import sqlite3
import nextcord

from core.db_utils import fetch_all
from core.shop.updaters import delete_role_from_shop
from core.marriage.update import (
    update_user_loveroom_id,
    update_couple_family_money,
    update_user_loveroom_expire_date
)
from core.marriage.getters import (
    get_family_money,
    get_marriage_config_month_loveroom_price
)
from core.money.updaters import update_user_balance
from nextcord.ext import tasks, commands


class TasksCog(commands.Cog):
    def __init__(self, client):
        self.client = client
        super().__init__()
        self.custom_shop_roles_expiration.start()
        self.give_roles_money.start()
        self.loveroom_expire_delete.start()

    @tasks.loop(minutes=8)
    async def loveroom_expire_delete(self):  # delete loveroom when expired
        now = datetime.datetime.now().timestamp()
        all_loverooms = await fetch_all(f"SELECT guild_id, loveroom_id, user_id, pair_id FROM marriage WHERE "
                                       f"loveroom_expire < {int(now)} "
                                       )
        if all_loverooms:
            for loveroom in all_loverooms:
                guild_id, loveroom_id, user_id, pair_id = loveroom[0], loveroom[1], loveroom[2], loveroom[3],
                try:
                    loveroom_cost = await get_marriage_config_month_loveroom_price(guild_id)
                    if await get_family_money(guild_id, user_id) >= loveroom_cost:
                        await update_couple_family_money(guild_id, user_id, pair_id, -loveroom_cost)
                        await update_user_loveroom_expire_date(guild_id, user_id, int(now + 86400 * 30))
                    else:
                        guild = await self.client.fetch_guild(guild_id)
                        room = await guild.fetch_channel(loveroom_id)
                        await update_user_loveroom_id(guild_id, user_id, 0)
                        await update_user_loveroom_id(guild_id, pair_id, 0)
                        await room.delete(reason="Loveroom expired")
                except Exception as e:
                    if isinstance(e, nextcord.errors.NotFound):
                        pass
                    else:
                        print(e)
                    continue
        else:
            return

    @tasks.loop(minutes=10)
    async def custom_shop_roles_expiration(self):
        now = datetime.datetime.now().timestamp()
        all_roles = await fetch_all(
            f"SELECT guild_id, expiration_date, role_id FROM custom_shop WHERE expiration_date < {int(now)}"
        )
        if all_roles:

            for role in all_roles:
                try:
                    guild = self.client.get_guild(role[0])
                    rol = nextcord.utils.get(guild.roles, id=role[2])
                    await rol.delete(reason="Custom role expired")
                    await delete_role_from_shop(guild, rol.id)

                except Exception as e:
                    print(e)
                    continue
        else:
            return

    @tasks.loop(hours=12)
    async def give_roles_money(self):
        rows = await fetch_all(
            f"SELECT role_id, income, guild_id FROM roles_money"
        )
        if not rows:
            return
        for row in rows:
            try:
                guild = self.client.get_guild(row[2])
                role = nextcord.utils.get(guild.roles, id=row[0])
            except:
                continue
            if role is not None:
                for member in guild.members:
                    if not member.bot:
                        if role.id in [role.id for role in member.roles]:
                            try:
                                await update_user_balance(row[2], member.id, row[1])
                            except TypeError as error:
                                print(error, row[2], member.id, row[1])

    @custom_shop_roles_expiration.before_loop
    @give_roles_money.before_loop
    @custom_shop_roles_expiration.before_loop
    async def before_printer(self):
        print("waiting...")
        await self.client.wait_until_ready()


def setup(client):
    client.add_cog(TasksCog(client))
