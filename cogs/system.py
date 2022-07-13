import nextcord
from typing import Optional
from nextcord import Interaction, SlashOption
from nextcord.ext import commands
from config import settings
import sqlite3
from core.locales.updaters import update_guild_locale
from core.checkers import is_locale_valid


class System(commands.Cog):
    def __init__(self, client):
        self.client = client

    @nextcord.slash_command(name='set_locale')
    async def __set_locale(self, interaction: Interaction, locale: Optional[str] = SlashOption(required=True)):
        """
        Parameters
        ----------
        interaction: Interaction
            The interaction object
        locale: Optional[str]
            Locale is the bot respond's language. Available locales: ru_ru/en_us
        before
            ID of message, BEFORE THIS message deletion will take place
        after
            ID of message, AFTER THIS message deletion will take place
        """
        if is_locale_valid(locale) is True:
            update_guild_locale(locale, interaction.guild.id)
            await interaction.response.send_message('done')
        else:
            await interaction.response.send_message('something gone wrong')


def setup(client):
    client.add_cog(System(client))
