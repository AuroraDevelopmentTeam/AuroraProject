from typing import Optional, Union
from io import BytesIO
import sqlite3

from PIL import Image
import cooldowns
from nextcord.ext import commands, menus, application_checks
from nextcord import Interaction, SlashOption, Permissions
import nextcord

from core.money.updaters import (
    update_guild_currency_symbol,
    update_guild_starting_balance,
    update_guild_payday_amount,
    update_user_balance,
    set_user_balance,
)
from core.money.getters import (
    get_user_balance,
    get_guild_currency_symbol,
    get_guild_starting_balance,
    get_guild_payday_amount,
)
from core.money.create import create_user_money_card
from core.checkers import is_str_or_emoji, is_role_in_shop
from core.locales.getters import (
    get_msg_from_locale_by_key, get_localized_description, get_localized_name)
from core.embeds import construct_basic_embed, construct_top_embed, DEFAULT_BOT_COLOR
from core.shop.writers import write_role_in_shop, delete_role_from_shop
from core.parsers import parse_server_roles
from core.ui.paginator import (
    MyEmbedFieldPageSource,
    MyEmbedDescriptionPageSource,
    SelectButtonMenuPages,
)


class Economics(commands.Cog):
    def __init__(self, client):
        self.client = client

    @nextcord.slash_command(
        name="add_money",
        description="Administrator's command to add the money on the balance of @User",
        name_localizations=get_localized_name("add_money"),
        description_localizations=get_localized_description("add_money"),
        default_member_permissions=Permissions(administrator=True),
    )
    @application_checks.has_permissions(manage_guild=True)
    async def __add_money(
        self,
        interaction: Interaction,
        user: Optional[nextcord.Member] = SlashOption(
            required=True,
            description="The discord's user, tag someone with @",
            description_localizations={"ru": "Пользователь дискорда, укажите кого-то @"},
        ),
        money: Optional[int] = SlashOption(
            required=True,
            description="Number of money the bot should send to user",
            description_localizations={"ru": "Количество денег, которое бот должен отправить"},
        ),
    ):
        if user.bot:
            return await interaction.response.send_message("bot_user_error")
        elif money >= 0 and isinstance(money, int):
            currency_symbol = get_guild_currency_symbol(interaction.guild.id)
            update_user_balance(interaction.guild.id, user.id, money)
            message = get_msg_from_locale_by_key(
                interaction.guild.id, f"{interaction.application_command.name}"
            )
            requested = get_msg_from_locale_by_key(interaction.guild.id, "requested_by")
            await interaction.response.send_message(
                embed=construct_basic_embed(
                    interaction.application_command.name,
                    f"{message} {user.mention}\n +__**{money}**__ {currency_symbol}",
                    f"{requested} {interaction.user}",
                    interaction.user.display_avatar,
                )
            )
        else:
            return await interaction.response.send_message("negative value error")

    @nextcord.slash_command(
        name="remove_money",
        description="Remove from @User's balance money",
        name_localizations=get_localized_name("remove_money"),
        description_localizations=get_localized_description("remove_money"),
        default_member_permissions=Permissions(administrator=True),
    )
    @application_checks.has_permissions(manage_guild=True)
    async def __remove_money(
        self,
        interaction: Interaction,
        user: Optional[nextcord.Member] = SlashOption(
            required=True,
            description="The discord's user, tag someone with @",
            description_localizations={"ru": "Пользователь дискорда, укажите кого-то @"},
        ),
        money: Optional[int] = SlashOption(
            required=True,
            description="Number of money the bot should take from user",
            description_localizations={"ru": "Количество денег, которое бот должен забрать"},
        ),
    ):
        if user.bot:
            return await interaction.response.send_message("bot_user_error")
        elif money >= 0 and isinstance(money, int):
            currency_symbol = get_guild_currency_symbol(interaction.guild.id)
            update_user_balance(interaction.guild.id, user.id, -money)
            message = get_msg_from_locale_by_key(
                interaction.guild.id, f"{interaction.application_command.name}"
            )
            requested = get_msg_from_locale_by_key(interaction.guild.id, "requested_by")
            await interaction.response.send_message(
                embed=construct_basic_embed(
                    interaction.application_command.name,
                    f"{message} {user.mention}\n -__**{money}**__ {currency_symbol}",
                    f"{requested} {interaction.user}",
                    interaction.user.display_avatar,
                )
            )
        else:
            return await interaction.response.send_message("negative value error")

    @nextcord.slash_command(
        name="balance",
        description="Show your or @User's balance",
        name_localizations=get_localized_name("balance"),
        description_localizations=get_localized_description("balance"),
        default_member_permissions=Permissions(send_messages=True),
    )
    async def __money(
        self,
        interaction: Interaction,
            user: Optional[nextcord.Member] = SlashOption(
                required=False,
                description="The discord's user, tag someone with @",
                description_localizations={"ru": "Пользователь дискорда, укажите кого-то @"},
            ),
    ):
        if user is None:
            user = interaction.user
        if user.bot:
            return await interaction.response.send_message("bot_user_error")
        avatar = BytesIO()
        await user.display_avatar.with_format("png").save(avatar)
        profile_picture = Image.open(avatar)
        file, embed = create_user_money_card(
            interaction.application_command.name.capitalize(),
            interaction.user,
            user,
            profile_picture,
            interaction.guild.id,
        )
        await interaction.response.send_message(embed=embed, file=file)

    @nextcord.slash_command(
        name="reset",
        description="Reset's server economics, "
                    "all user balances to starting balances",
        name_localizations=get_localized_name("reset"),
        description_localizations=get_localized_description("reset"),
        default_member_permissions=Permissions(administrator=True)
    )
    @application_checks.has_permissions(manage_guild=True)
    async def __reset(self, interaction: Interaction):
        """
        This is the reset slash command that will be the prefix of economical reset commands
        """
        pass

    @__reset.subcommand(
        name="balance",
        description="Reset's a members balance to standart value",
        name_localizations=get_localized_name("reset_balance"),
        description_localizations=get_localized_description("reset_balance"),
    )
    async def ___money(
        self,
        interaction: Interaction,
        user: Optional[nextcord.Member] = SlashOption(
            required=True,
            description="The discord's user, tag someone with @",
            description_localizations={"ru": "Пользователь дискорда, укажите кого-то @"}
        )
    ):
        if user.bot:
            return await interaction.response.send_message("bot_user_error")
        else:
            starting_balance = get_guild_starting_balance(interaction.guild.id)
            set_user_balance(interaction.guild.id, user.id, starting_balance)
            currency_symbol = get_guild_currency_symbol(interaction.guild.id)
            message = get_msg_from_locale_by_key(
                interaction.guild.id, f"reset_{interaction.application_command.name}"
            )
            message_2 = get_msg_from_locale_by_key(
                interaction.guild.id, f"reset_{interaction.application_command.name}_2"
            )
            requested = get_msg_from_locale_by_key(interaction.guild.id, "requested_by")
            await interaction.response.send_message(
                embed=construct_basic_embed(
                    interaction.application_command.name,
                    f"{message} {user.mention} {message_2} **{starting_balance}** {currency_symbol}",
                    f"{requested} {interaction.user}",
                    interaction.user.display_avatar,
                )
            )

    @__reset.subcommand(
        name="economics",
        description="Reset's server economics, "
        "all user balances to starting balances",
        name_localizations=get_localized_name("reset_economics"),
        description_localizations=get_localized_description("reset_economics")
    )
    async def __economics(self, interaction: Interaction):
        starting_balance = get_guild_starting_balance(interaction.guild.id)
        for member in interaction.guild.members:
            if not member.bot:
                set_user_balance(interaction.guild.id, member.id, starting_balance)
        currency_symbol = get_guild_currency_symbol(interaction.guild.id)
        message = get_msg_from_locale_by_key(
            interaction.guild.id, f"reset_{interaction.application_command.name}"
        )
        requested = get_msg_from_locale_by_key(interaction.guild.id, "requested_by")
        await interaction.response.send_message(
            embed=construct_basic_embed(
                interaction.application_command.name,
                f"{message} **{starting_balance}** {currency_symbol}",
                f"{requested} {interaction.user}",
                interaction.user.display_avatar,
            )
        )

    @nextcord.slash_command(
        name="timely",
        description="Get money per time",
        name_localizations=get_localized_name("timely"),
        description_localizations=get_localized_description("timely"),
        default_member_permissions=Permissions(send_messages=True)
    )
    @cooldowns.cooldown(1, 3600, bucket=cooldowns.SlashBucket.author)
    async def __timely(self, interaction: Interaction):
        payday_amount = get_guild_payday_amount(interaction.guild.id)
        update_user_balance(interaction.guild.id, interaction.user.id, payday_amount)
        currency_symbol = get_guild_currency_symbol(interaction.guild.id)
        message = get_msg_from_locale_by_key(
            interaction.guild.id, f"{interaction.application_command.name}"
        )
        requested = get_msg_from_locale_by_key(interaction.guild.id, "requested_by")
        await interaction.response.send_message(
            embed=construct_basic_embed(
                interaction.application_command.name,
                f"{message}" f"+__**{payday_amount}**__ {currency_symbol}",
                f"{requested} {interaction.user}",
                interaction.user.display_avatar,
            )
        )

    @nextcord.slash_command(
        name="give",
        description="Transfer your money from balance to other user",
        name_localizations=get_localized_name("give"),
        description_localizations=get_localized_description("give"),
        default_member_permissions=Permissions(send_messages=True)
    )
    async def __give(
        self,
        interaction: Interaction,
        user: Optional[nextcord.Member] = SlashOption(
            required=True,
            description="The discord's user, tag someone with @",
            description_localizations={"ru": "Пользователь дискорда, укажите кого-то @"}
        ),
        money: Optional[int] = SlashOption(
            required=True,
            description="Number of money you want to give @User",
            description_localizations={"ru": "Количество денег, которое вы хотите передать @Пользователю"},
        )
    ):
        if user.bot:
            return await interaction.response.send_message("bot_user_error")
        elif user == interaction.user:
            return await interaction.response.send_message("self choose error")
        elif money >= 0 and isinstance(money, int):
            balance = get_user_balance(interaction.guild.id, interaction.user.id)
            if balance < money:
                return await interaction.response.send_message("not_enough_money_error")
            else:
                update_user_balance(interaction.guild.id, interaction.user.id, -money)
                update_user_balance(interaction.guild.id, user.id, money)
                currency_symbol = get_guild_currency_symbol(interaction.guild.id)
                message = get_msg_from_locale_by_key(
                    interaction.guild.id, f"{interaction.application_command.name}"
                )
                requested = get_msg_from_locale_by_key(
                    interaction.guild.id, "requested_by"
                )
                await interaction.response.send_message(
                    embed=construct_basic_embed(
                        interaction.application_command.name,
                        f"__**{money}**__ {currency_symbol} {message} {user.mention}\n",
                        f"{requested} {interaction.user}",
                        interaction.user.display_avatar,
                    )
                )
        else:
            return await interaction.response.send_message("negative_value_error")

    @nextcord.slash_command(
        name="add-shop",
        description="Add role to shop",
        name_localizations=get_localized_name("add-shop"),
        description_localizations=get_localized_description("add-shop"),
        default_member_permissions=Permissions(administrator=True)
    )
    @application_checks.has_permissions(manage_guild=True)
    async def __add_shop(
        self,
        interaction: Interaction,
        role: Optional[nextcord.Role] = SlashOption(
            required=True,
            description="Discord role on your server",
            description_localizations={"ru": "Дискордовская роль на вашем сервере"},
        ),
        cost: Optional[int] = SlashOption(
            required=True,
            description="Number of money role will cost",
            description_localizations={"ru": "Количество денег, которое должна стоить роль"},
        )
    ):
        if cost < 0:
            return await interaction.response.send_message("negative value error")
        if is_role_in_shop(interaction.guild.id, role.id) is True:
            return await interaction.response.send_message("already in shop")
        write_role_in_shop(interaction.guild.id, role, cost)
        message = get_msg_from_locale_by_key(
            interaction.guild.id, f"{interaction.application_command.name}"
        )
        requested = get_msg_from_locale_by_key(interaction.guild.id, "requested_by")
        await interaction.response.send_message(
            embed=construct_basic_embed(
                interaction.application_command.name,
                f"{role.mention} {message}",
                f"{requested} {interaction.user}",
                interaction.user.display_avatar,
            )
        )

    @nextcord.slash_command(
        name="remove-shop",
        description="Remove role from shop",
        name_localizations=get_localized_name("remove-shop"),
        description_localizations=get_localized_description("remove-shop"),
        default_member_permissions=Permissions(administrator=True)
    )
    @application_checks.has_permissions(manage_guild=True)
    async def __remove_shop(
        self,
        interaction: Interaction,
        role: Optional[nextcord.Role] = SlashOption(
            required=True,
            description="Discord role on your server",
            description_localizations={"ru": "Дискордовская роль на вашем сервере"},
        )
    ):
        if is_role_in_shop(interaction.guild.id, role.id) is False:
            return await interaction.response.send_message("not in shop")
        delete_role_from_shop(interaction.guild.id, role)
        message = get_msg_from_locale_by_key(
            interaction.guild.id, f"{interaction.application_command.name}"
        )
        await interaction.response.send_message(
            embed=construct_basic_embed(
                interaction.application_command.name,
                f"{role.mention} {message}",
                f"{requested} {interaction.user}",
                interaction.user.display_avatar,
            )
        )

    @nextcord.slash_command(
        name="shop",
        description="show role shop menu",
        name_localizations=get_localized_name("shop"),
        description_localizations=get_localized_description("shop"),
        default_member_permissions=Permissions(send_messages=True)
    )
    async def __shop(self, interaction: Interaction):
        guild_roles = parse_server_roles(interaction.guild)
        pages = SelectButtonMenuPages(
            source=MyEmbedDescriptionPageSource(guild_roles),
            guild=interaction.guild,
            disabled=False,
        )
        await pages.start(interaction=interaction)


def setup(client):
    client.add_cog(Economics(client))
