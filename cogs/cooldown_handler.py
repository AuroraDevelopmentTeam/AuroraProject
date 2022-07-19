from cooldowns import CallableOnCooldown

import nextcord
from nextcord import Interaction
from nextcord.ext import commands


class CooldownHandler(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_application_command_error(self, interaction: Interaction, error):
        error = getattr(error, "original", error)

        if isinstance(error, CallableOnCooldown):
            await interaction.send(
                f"You are being rate-limited! Retry in `{error.retry_after}` seconds."
            )

        else:
            raise error


def setup(client):
    client.add_cog(CooldownHandler(client))
