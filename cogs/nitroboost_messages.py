import nextcord
from nextcord.ext import commands
from nextcord import Interaction
from nextcord.ext import menus

from core.nitro.getters import get_server_nitro_channel_id, get_server_nitro_state
from core.nitro.create import create_server_nitro_embed


class NitroBoostAnnouncement(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        if before.premium_since is None and after.premium_since is not None:
            print("boosted server")
            if not get_server_nitro_state(after.guild.id):
                return
            nitro_boost_channel_id = get_server_nitro_channel_id(after.guild.id)
            if nitro_boost_channel_id == 0:
                return
            nitro_boost_channel = self.client.get_channel(nitro_boost_channel_id)
            embed = create_server_nitro_embed(after, after.guild)
            await nitro_boost_channel.send(embed=embed)


def setup(client):
    client.add_cog(NitroBoostAnnouncement(client))
