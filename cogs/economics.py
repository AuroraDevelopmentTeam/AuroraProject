from nextcord.ext import commands
from nextcord import Interaction, SlashOption
import nextcord
from typing import Optional
from core.money.updaters import update_guild_currency_symbol, update_guild_starting_balance, \
    update_guild_payday_amount, update_user_balance
from core.money.getters import get_user_balance, get_guild_currency_symbol
from core.checkers import is_str_or_emoji
from core.locales.getters import get_msg_from_locale_by_key
from core.embeds import construct_basic_embed


class Economics(commands.Cog):
    def __init__(self, client):
        self.client = client

    @nextcord.slash_command(name="add_money", description="Add to @User number of money on balance")
    async def __add_money(self, interaction: Interaction,
                          user: Optional[nextcord.Member] = SlashOption(required=True),
                          money: Optional[int] = SlashOption(required=True)
                          ):
        """
        Parameters
        ----------
        interaction: Interaction
            The interaction object
        user: Optional[nextcord.Member]
            Tag discords member with @
        money: Optional[int]
            Number of money the bot should send to user
        """
        if user.bot:
            return await interaction.response.send_message('bot_user_error')
        elif money >= 0 and isinstance(money, int):
            currency_symbol = get_guild_currency_symbol(interaction.guild.id)
            update_user_balance(interaction.guild.id, user.id, money)
            message = get_msg_from_locale_by_key(interaction.guild.id, f"{interaction.application_command.name}")
            requested = get_msg_from_locale_by_key(interaction.guild.id, 'requested_by')
            await interaction.response.send_message(
                embed=construct_basic_embed(interaction.application_command.name,
                                            f"{message} {user.mention}\n +__**{money}**__ {currency_symbol}",
                                            f"{requested} {interaction.user}",
                                            interaction.user.display_avatar))
        else:
            return await interaction.response.send_message('negative value error')

    @nextcord.slash_command(name="remove_money", description="Remove from @User's balance money")
    async def __remove_money(self, interaction: Interaction,
                             user: Optional[nextcord.Member] = SlashOption(required=True),
                             money: Optional[int] = SlashOption(required=True)
                             ):
        """
        Parameters
        ----------
        interaction: Interaction
            The interaction object
        user: Optional[nextcord.Member]
            Tag discords member with @
        money: Optional[int]
            Number of money the bot should remove from user
        """
        if user.bot:
            return await interaction.response.send_message('bot_user_error')
        elif money >= 0 and isinstance(money, int):
            currency_symbol = get_guild_currency_symbol(interaction.guild.id)
            update_user_balance(interaction.guild.id, user.id, -money)
            message = get_msg_from_locale_by_key(interaction.guild.id, f"{interaction.application_command.name}")
            requested = get_msg_from_locale_by_key(interaction.guild.id, 'requested_by')
            await interaction.response.send_message(
                embed=construct_basic_embed(interaction.application_command.name,
                                            f"{message} {user.mention}\n -__**{money}**__ {currency_symbol}",
                                            f"{requested} {interaction.user}",
                                            interaction.user.display_avatar))
        else:
            return await interaction.response.send_message('negative value error')

    @nextcord.slash_command(name="money", description="Show your or @User's balance")
    async def __money(self, interaction: Interaction, user: Optional[nextcord.Member] = SlashOption(required=False)):
        if user is None:
            user = interaction.user
        elif user.bot:
            return await interaction.response.send_message('bot_user_error')
        currency_symbol = get_guild_currency_symbol(interaction.guild.id)
        balance = get_user_balance(interaction.guild.id, user.id)
        message = get_msg_from_locale_by_key(interaction.guild.id, f"{interaction.application_command.name}")
        requested = get_msg_from_locale_by_key(interaction.guild.id, 'requested_by')
        await interaction.response.send_message(
            embed=construct_basic_embed(f'{interaction.application_command.name} - {user}',
                                        f"{message} __**{balance}**__ {currency_symbol}",
                                        f"{requested} {interaction.user}",
                                        user.display_avatar))

    @nextcord.slash_command(name="reset")
    async def __reset(self, interaction: Interaction):
        """
        This is the reset slash command that will be the prefix of economical set commands below.
        """
        pass

    @__reset.subcommand(name="money", description="Reset's a members balance to standart value")
    async def ___money(self, interaction: Interaction):
        await interaction.response.send_message('test')


def setup(client):
    client.add_cog(Economics(client))
