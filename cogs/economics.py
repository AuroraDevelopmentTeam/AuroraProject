from nextcord.ext import commands


class Economics(commands.Cog):
    def __init__(self, client):
        self.client = client


def setup(client):
    client.add_cog(Economics(client))
