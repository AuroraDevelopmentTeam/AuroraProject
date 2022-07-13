from nextcord.ext import commands


class Levels(commands.Cog):
    def __init__(self, client):
        self.client = client

        
def setup(client):
    client.add_cog(Levels(client))
