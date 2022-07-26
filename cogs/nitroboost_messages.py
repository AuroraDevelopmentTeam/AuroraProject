import nextcord
from nextcord.ext import commands
from nextcord import Interaction
from nextcord.ext import menus
from core.ui.paginator import MyEmbedFieldPageSource


class NitroBoostAnnouncement(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        if before.premium_since is None and after.premium_since is not None:
            print('boosted server')
            print(after.guild.id)


def setup(client):
    client.add_cog(NitroBoostAnnouncement(client))
