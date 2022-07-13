from nextcord.ext import commands
from nextcord import Interaction, SlashOption
import nextcord
from typing import Optional
from core.money.updaters import update_guild_currency_symbol, update_guild_starting_balance
from core.checkers import is_str_or_emoji


class Economics(commands.Cog):
    def __init__(self, client):
        self.client = client

    @nextcord.slash_command(name="set_currency", description="Set server's currency to new symbol")
    async def __set_currency(self, interaction: Interaction,
                             currency_symbol: Optional[str] = SlashOption(required=True)):
        """
        Parameters
        ----------
        interaction: Interaction
            The interaction object
        currency_symbol: Optional[str]
            New symbol for currency
        """
        if is_str_or_emoji(currency_symbol):
            update_guild_currency_symbol(interaction.guild.id, currency_symbol)
            await interaction.response.send_message('set')
        else:
            await interaction.response.send_message('error')

    @nextcord.slash_command(name="set_start_balance", description="Set's server starting balance to new number")
    async def __set_start_balance(self, interaction: Interaction, balance: Optional[int] = SlashOption(required=True)):
        """
        Parameters
        ----------
        interaction: Interaction
            The interaction object
        balance: Optional[int]
            New guests of server will start with this number of money on their balance
        """
        if isinstance(balance, int):
            update_guild_starting_balance(interaction.guild.id, balance)
            await interaction.response.send_message('set')
        else:
            await interaction.response.send_message('error')


def setup(client):
    client.add_cog(Economics(client))
