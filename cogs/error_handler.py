import locale
import datetime

from cooldowns import CallableOnCooldown

import nextcord
from nextcord import Interaction
from nextcord.ext import commands
from nextcord.ext.application_checks import ApplicationMissingPermissions

from core.locales.getters import get_msg_from_locale_by_key


class ErrorHandler(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_application_command_error(self, interaction: Interaction, error):
        error = getattr(error, "original", error)

        if isinstance(error, CallableOnCooldown):
            locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')
            return await interaction.send(
                f"{get_msg_from_locale_by_key(interaction.guild.id, 'rate_limit')} "
                f"`{datetime.timedelta(seconds=int(error.retry_after))}`"
            )

        elif isinstance(error, ApplicationMissingPermissions):
            msg = get_msg_from_locale_by_key(interaction.guild.id, "ApplicationMissingPermissions")
            return await interaction.send(f"{msg}\n`{error}`")
        else:
            raise error


def setup(client):
    client.add_cog(ErrorHandler(client))
