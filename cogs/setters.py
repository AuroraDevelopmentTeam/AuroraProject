import nextcord
from nextcord import Interaction, SlashOption
from nextcord.ext import commands

from typing import Optional
from config import settings
import sqlite3

from core.embeds import construct_basic_embed
from core.locales.getters import get_msg_from_locale_by_key, get_keys_value_in_locale
from core.money.updaters import update_guild_currency_symbol, update_guild_starting_balance, \
    update_guild_payday_amount, update_user_balance
from core.locales.updaters import update_guild_locale
from core.checkers import is_locale_valid, is_str_or_emoji
from core.levels.updaters import set_server_level_up_messages_state


class Setters(commands.Cog):
    def __init__(self, client):
        self.client = client

    @nextcord.slash_command(name="set")
    async def __set(self, interaction: Interaction):
        """
        This is the set slash command that will be the prefix of economical set commands below.
        """
        pass

    @__set.subcommand(name='locale', description="Choose bot's respond's main language on your server!")
    async def __locale(self, interaction: Interaction, locale: str = SlashOption(
        name="picker",
        choices={"russian": "ru_ru", "english": "en_us"},
        required=True
    )):
        """
        Parameters
        ----------
        interaction: Interaction
            The interaction object
        locale: Optional[str]
            Locale is the bot respond language. Available locales: ru_ru/en_us
        """
        if is_locale_valid(locale) is True:
            update_guild_locale(locale, interaction.guild.id)
            message = get_msg_from_locale_by_key(interaction.guild.id, f"set_{interaction.application_command.name}")
            requested = get_msg_from_locale_by_key(interaction.guild.id, 'requested_by')
            await interaction.response.send_message(
                embed=construct_basic_embed(interaction.application_command.name,
                                            f"{message} **{locale}**",
                                            f"{requested} {interaction.user}",
                                            interaction.user.display_avatar))
        else:
            await interaction.response.send_message('something gone wrong')

    @__set.subcommand(name="currency", description="Set server's currency to new symbol")
    async def __currency(self, interaction: Interaction,
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
            message = get_msg_from_locale_by_key(interaction.guild.id, f"set_{interaction.application_command.name}")
            requested = get_msg_from_locale_by_key(interaction.guild.id, 'requested_by')
            await interaction.response.send_message(
                embed=construct_basic_embed(interaction.application_command.name,
                                            f"{message} **{currency_symbol}**",
                                            f"{requested} {interaction.user}",
                                            interaction.user.display_avatar))
        else:
            await interaction.response.send_message('error')

    @__set.subcommand(name="start_balance", description="Set's server starting balance to new number")
    async def __start_balance(self, interaction: Interaction, balance: Optional[int] = SlashOption(required=True)):
        """
        Parameters
        ----------
        interaction: Interaction
            The interaction object
        balance: Optional[int]
            New guests of server will start with this number of money on their balance
        """
        if balance >= 0 and isinstance(balance, int):
            update_guild_starting_balance(interaction.guild.id, balance)
            message = get_msg_from_locale_by_key(interaction.guild.id, f"set_{interaction.application_command.name}")
            requested = get_msg_from_locale_by_key(interaction.guild.id, 'requested_by')
            await interaction.response.send_message(
                embed=construct_basic_embed(interaction.application_command.name,
                                            f"{message} **{balance}**",
                                            f"{requested} {interaction.user}",
                                            interaction.user.display_avatar))
        else:
            await interaction.response.send_message('error')

    @__set.subcommand(name="timely_amount", description="Set's server payday amount per time with /timely "
                                                        "command")
    async def __payday_amount(self, interaction: Interaction,
                              payday_amount: Optional[int] = SlashOption(required=True)):
        """
        Parameters
        ----------
        interaction: Interaction
            The interaction object
        payday_amount: Optional[int]
            Members of server will get this number of money on their balance with /timely command
        """
        if payday_amount >= 0 and isinstance(payday_amount, int):
            update_guild_payday_amount(interaction.guild.id, payday_amount)
            message = get_msg_from_locale_by_key(interaction.guild.id, f"set_{interaction.application_command.name}")
            requested = get_msg_from_locale_by_key(interaction.guild.id, 'requested_by')
            await interaction.response.send_message(
                embed=construct_basic_embed(interaction.application_command.name,
                                            f"{message} **{payday_amount}**",
                                            f"{requested} {interaction.user}",
                                            interaction.user.display_avatar))
        else:
            await interaction.response.send_message('error')

    @__set.subcommand(name="level_up_messages", description="Turn on or turn off level up messages on your server")
    async def __level_up_messages_state(self, interaction: Interaction, level_up_messages_state: int = SlashOption(
        name="picker",
        choices={"turn on": 1, "turn off": 0},
        required=True
    )):
        set_server_level_up_messages_state(interaction.guild.id, bool(level_up_messages_state))
        message = get_msg_from_locale_by_key(interaction.guild.id, f"set_{interaction.application_command.name}")
        requested = get_msg_from_locale_by_key(interaction.guild.id, 'requested_by')
        if level_up_messages_state is True:
            level_up_messages_state = "enabled"
        else:
            level_up_messages_state = "disabled"
        await interaction.response.send_message(
            embed=construct_basic_embed(interaction.application_command.name,
                                        f"{message} **{level_up_messages_state}**",
                                        f"{requested} {interaction.user}",
                                        interaction.user.display_avatar))


def setup(client):
    client.add_cog(Setters(client))
