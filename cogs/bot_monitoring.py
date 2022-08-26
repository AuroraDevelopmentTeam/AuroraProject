import sdc_api_py
from nextcord.ext import commands
from dotenv import load_dotenv
import os

load_dotenv()

SDC_TOKEN = os.getenv("SDC_TOKEN")


class BotsSDC(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        """
        bots = sdc_api_py.Bots(self.client, SDC_TOKEN, fork_name="nextcord")
        bots.create_loop()
        """


def setup(client):
    client.add_cog(BotsSDC(client))
