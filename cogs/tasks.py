import datetime
import sqlite3
import nextcord

from core.shop.updaters import delete_role_from_shop
from nextcord.ext import tasks, commands


class TasksCog(commands.Cog):
    def __init__(self, client):
        self.client = client
        super().__init__()
        self.custom_shop_roles_expiration.start()

    @tasks.loop(minutes=10)
    async def custom_shop_roles_expiration(self):
        now = datetime.datetime.now().timestamp()
        db = sqlite3.connect("./databases/main.sqlite")
        cursor = db.cursor()
        all_roles = cursor.execute(
            f"SELECT guild_id, expiration_date, role_id FROM custom_shop WHERE expiration_date < {int(now)}"
        ).fetchall()
        if all_roles != []:

            print(all_roles)
            for role in all_roles:
                try:
                    guild = self.client.get_guild(role[0])
                    rol = nextcord.utils.get(guild.roles, id=role[2])
                    await rol.delete(reason="Role expired")
                    delete_role_from_shop(guild, rol.id)

                except Exception as e:
                    print(e)
                    continue
        else:
            print(all_roles)

    @custom_shop_roles_expiration.before_loop
    async def before_printer(self):
        print("waiting...")
        await self.client.wait_until_ready()


def setup(client):
    client.add_cog(TasksCog(client))
