from typing import Optional, Union
from io import BytesIO
import sqlite3

from PIL import Image
import cooldowns
from nextcord.ext import commands
from nextcord import Interaction, SlashOption, Permissions
import nextcord

from core.money.updaters import update_guild_currency_symbol, update_guild_starting_balance, \
    update_guild_payday_amount, update_user_balance, set_user_balance
from core.money.getters import get_user_balance, get_guild_currency_symbol, get_guild_starting_balance, \
    get_guild_payday_amount
from core.money.create import create_user_money_card
from core.checkers import is_str_or_emoji, is_role_in_shop
from core.locales.getters import get_msg_from_locale_by_key
from core.embeds import construct_basic_embed, construct_top_embed, DEFAULT_BOT_COLOR
from core.shop.writers import write_role_in_shop, delete_role_from_shop
from core.parsers import parse_server_roles


class Dropdown(nextcord.ui.Select):
    def __init__(self, guild: nextcord.Guild, disabled: bool):
        self.guild = guild
        self.price = []
        self.role_list = []
        roles = parse_server_roles(guild, False)
        sel_opt = []
        if len(roles) > 0:
            for i in range(len(roles)):
                self.price.append(roles[i][1])
                self.role_list.append(roles[i][0])
                sel_opt.append(nextcord.SelectOption(label=f'{i + 1}',
                                                     description=f'{roles[i][0].name} {roles[i][1]}'))
            super().__init__(placeholder="Select role from shop", min_values=1, max_values=1, options=sel_opt,
                             disabled=disabled)
        else:
            sel_opt = [nextcord.SelectOption(label=f'...', description='...')]
            super().__init__(placeholder="Select role from shop", min_values=1, max_values=1, options=sel_opt,
                             disabled=disabled)

    async def callback(self, interaction: Interaction):
        embed = nextcord.Embed(color=DEFAULT_BOT_COLOR)
        msg = get_msg_from_locale_by_key(self.guild.id, "shop")
        if self.values[0] != '...':
            balance = get_user_balance(interaction.guild.id, interaction.user.id)
            if balance < (self.price[int(self.values[0]) - 1]):
                embed.add_field(name='error', value='not_enough_money_error')
                return await interaction.message.edit(embed=embed,
                                                      view=DropdownView(interaction.guild, interaction.user,
                                                                        disabled=True))
            if self.role_list[int(self.values[0]) - 1] in interaction.user.roles:
                embed.add_field(name='error', value='already have role')
                return await interaction.message.edit(embed=embed,
                                                      view=DropdownView(interaction.guild, interaction.user,
                                                                        disabled=True))
            await interaction.user.add_roles(self.role_list[int(self.values[0]) - 1])
            embed.add_field(name='Shop', value=f'{msg} {self.role_list[int(self.values[0]) - 1].mention}')
            update_user_balance(interaction.guild.id, interaction.user.id, -(self.price[int(self.values[0]) - 1]))
            balance = get_user_balance(interaction.guild.id, interaction.user.id)
            msg = get_msg_from_locale_by_key(interaction.guild.id, "on_balance")
            embed.set_footer(text=f"{msg} {balance}", icon_url=interaction.user.display_avatar)
        else:
            embed.add_field(name='Shop', value=f'ヾ( ￣O￣)ツ	')
        await interaction.message.edit(embed=embed,
                                       view=DropdownView(interaction.guild, interaction.user, disabled=True))


class DropdownView(nextcord.ui.View):
    def __init__(self, guild: nextcord.Guild, author: Union[nextcord.Member, nextcord.User], disabled: bool):
        self.guild = guild
        self.author = author
        self.disabled = disabled
        super().__init__()
        self.add_item(Dropdown(guild=self.guild, disabled=disabled))

    async def interaction_check(self, interaction: Interaction) -> bool:
        if interaction.user != self.author:
            return False
        return True


class Economics(commands.Cog):
    def __init__(self, client):
        self.client = client

    @nextcord.slash_command(name="add_money", description="Add to @User number of money on balance",
                            default_member_permissions=Permissions(administrator=True))
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

    @nextcord.slash_command(name="remove_money", description="Remove from @User's balance money",
                            default_member_permissions=Permissions(administrator=True))
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

    @nextcord.slash_command(name="money", description="Show your or @User's balance",
                            default_member_permissions=Permissions(send_messages=True))
    async def __money(self, interaction: Interaction, user: Optional[nextcord.Member] = SlashOption(required=False)):
        if user is None:
            user = interaction.user
        if user.bot:
            return await interaction.response.send_message('bot_user_error')
        avatar = BytesIO()
        await user.display_avatar.with_format("png").save(avatar)
        profile_picture = Image.open(avatar)
        file, embed = create_user_money_card(interaction.application_command.name.capitalize(),
                                             interaction.user, user, profile_picture, interaction.guild.id)
        await interaction.response.send_message(embed=embed, file=file)

    @nextcord.slash_command(name="reset", default_member_permissions=Permissions(administrator=True))
    async def __reset(self, interaction: Interaction):
        """
        This is the reset slash command that will be the prefix of economical set commands below.
        """
        pass

    @__reset.subcommand(name="money", description="Reset's a members balance to standart value")
    async def ___money(self, interaction: Interaction, user: Optional[nextcord.Member] = SlashOption(required=True)):
        if user.bot:
            return await interaction.response.send_message('bot_user_error')
        else:
            starting_balance = get_guild_starting_balance(interaction.guild.id)
            set_user_balance(interaction.guild.id, user.id, starting_balance)
            await interaction.response.send_message('done')

    @__reset.subcommand(name="economics", description="Reset's server economics, "
                                                      "all user balances to starting balances")
    async def __economics(self, interaction: Interaction):
        for member in interaction.guild.members:
            if not member.bot:
                starting_balance = get_guild_starting_balance(interaction.guild.id)
                set_user_balance(interaction.guild.id, member.id, starting_balance)
        await interaction.response.send_message('done')

    @nextcord.slash_command(name="timely", description="Get money per time",
                            default_member_permissions=Permissions(send_messages=True))
    @cooldowns.cooldown(1, 3600, bucket=cooldowns.SlashBucket.author)
    async def __timely(self, interaction: Interaction):
        payday_amount = get_guild_payday_amount(interaction.guild.id)
        update_user_balance(interaction.guild.id, interaction.user.id, payday_amount)
        currency_symbol = get_guild_currency_symbol(interaction.guild.id)
        message = get_msg_from_locale_by_key(interaction.guild.id, f"{interaction.application_command.name}")
        requested = get_msg_from_locale_by_key(interaction.guild.id, 'requested_by')
        await interaction.response.send_message(
            embed=construct_basic_embed(interaction.application_command.name,
                                        f"{message}"
                                        f"+__**{payday_amount}**__ {currency_symbol}",
                                        f"{requested} {interaction.user}",
                                        interaction.user.display_avatar))

    @nextcord.slash_command(name="give", description="Transfer your money from balance to other user",
                            default_member_permissions=Permissions(send_messages=True))
    async def __give(self, interaction: Interaction, user: Optional[nextcord.Member] = SlashOption(required=True),
                     money: Optional[int] = SlashOption(required=True)):
        """
        Parameters
        ----------
        interaction: Interaction
            The interaction object
        user: Optional[nextcord.Member]
            Tag discords member with @
        money: Optional[int]
            Number of money you will tranfer to @User
        """
        if user.bot:
            return await interaction.response.send_message('bot_user_error')
        elif user == interaction.user:
            return await interaction.response.send_message('self choose error')
        elif money >= 0 and isinstance(money, int):
            balance = get_user_balance(interaction.guild.id, interaction.user.id)
            if balance < money:
                return await interaction.response.send_message('not_enough_money_error')
            else:
                update_user_balance(interaction.guild.id, interaction.user.id, -money)
                update_user_balance(interaction.guild.id, user.id, money)
                currency_symbol = get_guild_currency_symbol(interaction.guild.id)
                message = get_msg_from_locale_by_key(interaction.guild.id, f"{interaction.application_command.name}")
                requested = get_msg_from_locale_by_key(interaction.guild.id, 'requested_by')
                await interaction.response.send_message(
                    embed=construct_basic_embed(interaction.application_command.name,
                                                f"__**{money}**__ {currency_symbol} {message} {user.mention}\n",
                                                f"{requested} {interaction.user}",
                                                interaction.user.display_avatar))
        else:
            return await interaction.response.send_message('negative_value_error')

    @nextcord.slash_command(name="add-shop", description="Add role to shop")
    async def __add_shop(self, interaction: Interaction, role: Optional[nextcord.Role] = SlashOption(required=True),
                         cost: Optional[int] = SlashOption(required=True)):
        if cost < 0:
            return await interaction.response.send_message('negative value error')
        if is_role_in_shop(interaction.guild.id, role.id) is True:
            return await interaction.response.send_message('already in shop')
        write_role_in_shop(interaction.guild.id, role, cost)
        message = get_msg_from_locale_by_key(interaction.guild.id, f"{interaction.application_command.name}")
        requested = get_msg_from_locale_by_key(interaction.guild.id, 'requested_by')
        await interaction.response.send_message(
            embed=construct_basic_embed(interaction.application_command.name,
                                        f"{role.mention} {message}",
                                        f"{requested} {interaction.user}",
                                        interaction.user.display_avatar))

    @nextcord.slash_command(name="remove-shop", description="Remove role from shop")
    async def __remove_shop(self, interaction: Interaction, role: Optional[nextcord.Role] = SlashOption(required=True)):
        if is_role_in_shop(interaction.guild.id, role.id) is False:
            return await interaction.response.send_message('not in shop')
        delete_role_from_shop(interaction.guild.id, role)
        message = get_msg_from_locale_by_key(interaction.guild.id, f"{interaction.application_command.name}")
        await interaction.response.send_message(
            embed=construct_basic_embed(interaction.application_command.name,
                                        f"{role.mention} {message}",
                                        f"{requested} {interaction.user}",
                                        interaction.user.display_avatar))

    @nextcord.slash_command(name="shop", description="show role shop menu")
    async def __shop(self, interaction: Interaction):
        guild_roles = parse_server_roles(interaction.guild)
        currency_symbol = get_guild_currency_symbol(interaction.guild.id)
        requested = get_msg_from_locale_by_key(interaction.guild.id, 'requested_by')
        await interaction.response.send_message(
            embed=construct_top_embed(interaction.application_command.name, guild_roles,
                                      f"{requested} {interaction.user}", interaction.user.display_avatar,
                                      currency_symbol, interaction.guild),
            view=DropdownView(interaction.guild, interaction.user, False))


def setup(client):
    client.add_cog(Economics(client))
