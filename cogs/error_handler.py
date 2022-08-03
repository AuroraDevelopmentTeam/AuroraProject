from cooldowns import CallableOnCooldown

import nextcord
from nextcord import Interaction
from nextcord.ext import commands
from nextcord.ext.application_checks import ApplicationMissingPermissions


class ErrorHandler(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_application_command_error(self, interaction: Interaction, error):
        error = getattr(error, "original", error)

        if isinstance(error, CallableOnCooldown):
            return await interaction.send(
                f"You are being rate-limited! Retry in `{error.retry_after}` seconds."
            )

        elif isinstance(error, ApplicationMissingPermissions):
            return await interaction.send(f"ApplicationMissingPermissions\n`{error}`")
        else:
            raise error


def setup(client):
    client.add_cog(ErrorHandler(client))
