import nextcord
from nextcord.ext import commands


class UserVoiceHandler(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.voice_rooms = {}


def setup(client):
    client.add_cog(UserVoiceHandler(client))
