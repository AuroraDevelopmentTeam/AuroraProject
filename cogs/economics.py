import datetime
from typing import Optional, Union, Coroutine, Any
from io import BytesIO
import sqlite3

from PIL import Image
import cooldowns
from nextcord.ext import commands, menus, application_checks, tasks
from nextcord.abc import GuildChannel
from nextcord import Interaction, SlashOption, Permissions
import nextcord

import config
from core.money.updaters import (
    update_guild_currency_symbol,
    update_guild_starting_balance,
    update_guild_payday_amount,
    update_user_balance,
    set_user_balance,
    update_guild_msg_cooldown,
    update_guild_min_max_msg_income,
    update_guild_min_max_voice_income,
    update_guild_voice_minutes_for_money,
)
from core.money.getters import (
    get_user_balance,
    get_guild_currency_symbol,
    get_guild_starting_balance,
    get_guild_payday_amount,
    list_income_roles,
)
from core.money.writers import (
    write_role_in_income,
    delete_role_from_income,
    write_channel_in_config,
)
from core.money.create import create_user_money_card
from core.checkers import (
    is_str_or_emoji,
    is_role_in_shop,
    is_role_in_income,
    is_channel_in_config,
)
from core.locales.getters import (
    get_msg_from_locale_by_key,
    get_localized_description,
    get_localized_name,
    localize_name,
)
from core.embeds import construct_basic_embed, construct_top_embed, DEFAULT_BOT_COLOR
from core.shop.writers import (
    write_role_in_shop,
    write_role_in_custom_shop,
    delete_role_from_shop,
)
from core.shop.getters import custom_shop_embed, get_custom_shop_roles_limit

from core.parsers import parse_server_roles
from core.ui.paginator import (
    MyEmbedFieldPageSource,
    MyEmbedDescriptionPageSource,
    SelectButtonMenuPages,
)
from core.errors import (
    construct_error_negative_value_embed,
    construct_error_bot_user_embed,
    construct_error_self_choose_embed,
    construct_error_not_enough_embed,
    construct_error_forbidden_embed,
)


class AutorolesList(menus.ListPageSource):
    def __init__(self, data, guild_id):
        self.guild_id = guild_id
        super().__init__(data, per_page=6)

    async def format_page(self, menu, entries) -> nextcord.Embed:
        embed = nextcord.Embed(
            title=localize_name(self.guild_id, "income").capitalize(),
            color=DEFAULT_BOT_COLOR,
        )
        for entry in entries:
            embed.add_field(name=entry[0], value=entry[1], inline=False)
        embed.set_footer(text=f"{menu.current_page + 1}/{self.get_max_pages()}")
        return embed


class NoStopButtonMenuPages(menus.ButtonMenuPages, inherit_buttons=False):
    def __init__(self, source, timeout=60):
        super().__init__(source, timeout=timeout)

        # Add the buttons we want
        self.add_item(menus.MenuPaginationButton(emoji=self.FIRST_PAGE))
        self.add_item(menus.MenuPaginationButton(emoji=self.PREVIOUS_PAGE))
        self.add_item(menus.MenuPaginationButton(emoji=self.NEXT_PAGE))
        self.add_item(menus.MenuPaginationButton(emoji=self.LAST_PAGE))

        # Disable buttons that are unavailable to be pressed at the start
        self._disable_unavailable_buttons()


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
            description_localizations={
                "ru": "Пользователь дискорда, укажите кого-то @"
            },
        ),
        money: Optional[int] = SlashOption(
            required=True,
            description="Number of money the bot should send to user",
            description_localizations={
                "ru": "Количество денег, которое бот должен отправить"
            },
        ),
    ):
        if user.bot:
            return await interaction.response.send_message(
                embed=construct_error_bot_user_embed(
                    get_msg_from_locale_by_key(interaction.guild.id, "bot_user_error"),
                    self.client.user.avatar.url,
                )
            )
        elif money > 0 and isinstance(money, int):
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
                    interaction.guild.id,
                )
            )
        else:
            return await interaction.response.send_message(
                embed=construct_error_negative_value_embed(
                    get_msg_from_locale_by_key(
                        interaction.guild.id, "negative_value_error"
                    ),
                    self.client.user.avatar.url,
                    money,
                )
            )

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
            description_localizations={
                "ru": "Пользователь дискорда, укажите кого-то @"
            },
        ),
        money: Optional[int] = SlashOption(
            required=True,
            description="Number of money the bot should take from user",
            description_localizations={
                "ru": "Количество денег, которое бот должен забрать"
            },
        ),
    ):
        if user.bot:
            return await interaction.response.send_message(
                embed=construct_error_bot_user_embed(
                    get_msg_from_locale_by_key(interaction.guild.id, "bot_user_error"),
                    self.client.user.avatar.url,
                )
            )
        elif money > 0 and isinstance(money, int):
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
                    interaction.guild.id,
                )
            )
        else:
            return await interaction.response.send_message(
                embed=construct_error_negative_value_embed(
                    get_msg_from_locale_by_key(
                        interaction.guild.id, "negative_value_error"
                    ),
                    self.client.user.avatar.url,
                    money,
                )
            )

    @nextcord.slash_command(
        name="balance",
        description="Show your or @User's balance",
        name_localizations=get_localized_name("balance"),
        description_localizations=get_localized_description("balance"),
        default_member_permissions=Permissions(send_messages=True),
    )
    @cooldowns.cooldown(1, 5, bucket=cooldowns.SlashBucket.author)
    async def __money(
        self,
        interaction: Interaction,
        user: Optional[nextcord.Member] = SlashOption(
            required=False,
            description="The discord's user, tag someone with @",
            description_localizations={
                "ru": "Пользователь дискорда, укажите кого-то @"
            },
        ),
    ):
        if user is None:
            user = interaction.user
        if user.bot:
            return await interaction.response.send_message(
                embed=construct_error_bot_user_embed(
                    get_msg_from_locale_by_key(interaction.guild.id, "bot_user_error"),
                    self.client.user.avatar.url,
                )
            )
        await interaction.response.defer()
        avatar = BytesIO()
        await user.display_avatar.with_format("png").save(avatar)
        profile_picture = Image.open(avatar)
        file, embed = create_user_money_card(
            interaction.application_command.name,
            interaction.user,
            user,
            profile_picture,
            interaction.guild.id,
        )
        await interaction.followup.send(embed=embed, file=file)

    @nextcord.slash_command(
        name="reset",
        description="Reset's server economics, "
        "all user balances to starting balances",
        name_localizations=get_localized_name("reset"),
        description_localizations=get_localized_description("reset"),
        default_member_permissions=Permissions(administrator=True),
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
            description_localizations={
                "ru": "Пользователь дискорда, укажите кого-то @"
            },
        ),
    ):
        if user.bot:
            return await interaction.response.send_message(
                embed=construct_error_bot_user_embed(
                    get_msg_from_locale_by_key(interaction.guild.id, "bot_user_error"),
                    self.client.user.avatar.url,
                )
            )
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
                    interaction.guild.id,
                )
            )

    @__reset.subcommand(
        name="economics",
        description="Reset's server economics, "
        "all user balances to starting balances",
        name_localizations=get_localized_name("reset_economics"),
        description_localizations=get_localized_description("reset_economics"),
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
                interaction.guild.id,
            )
        )

    @nextcord.slash_command(
        name="timely",
        description="Get money per time",
        name_localizations=get_localized_name("timely"),
        description_localizations=get_localized_description("timely"),
        default_member_permissions=Permissions(send_messages=True),
    )
    @cooldowns.cooldown(1, 10800, bucket=cooldowns.SlashBucket.author)
    async def __timely(self, interaction: Interaction):
        payday_amount = get_guild_payday_amount(interaction.guild.id)
        update_user_balance(interaction.guild.id, interaction.user.id, payday_amount)
        currency_symbol = get_guild_currency_symbol(interaction.guild.id)
        message = get_msg_from_locale_by_key(
            interaction.guild.id, f"{interaction.application_command.name}"
        )
        requested = get_msg_from_locale_by_key(interaction.guild.id, "requested_by")
        embed = construct_basic_embed(
            interaction.application_command.name,
            f"{message}" f"+__**{payday_amount}**__ {currency_symbol}",
            f"{requested} {interaction.user}",
            interaction.user.display_avatar,
            interaction.guild.id,
        )
        embed.set_thumbnail(
            url="https://cdn.discordapp.com/attachments/996084073569194084/996084305031872574/white_clock.png"
        )
        embed.set_thumbnail(
            url="https://cdn.discordapp.com/attachments/996084073569194084/996084305031872574"
            "/white_clock.png"
        )
        await interaction.response.send_message(embed=embed)

    @nextcord.slash_command(
        name="give",
        description="Transfer your money from balance to other user",
        name_localizations=get_localized_name("give"),
        description_localizations=get_localized_description("give"),
        default_member_permissions=Permissions(send_messages=True),
    )
    async def __give(
        self,
        interaction: Interaction,
        user: Optional[nextcord.Member] = SlashOption(
            required=True,
            description="The discord's user, tag someone with @",
            description_localizations={
                "ru": "Пользователь дискорда, укажите кого-то @"
            },
        ),
        money: Optional[int] = SlashOption(
            required=True,
            description="Number of money you want to give @User",
            description_localizations={
                "ru": "Количество денег, которое вы хотите передать @Пользователю"
            },
        ),
    ):
        if user.bot:
            return await interaction.response.send_message(
                embed=construct_error_bot_user_embed(
                    get_msg_from_locale_by_key(interaction.guild.id, "bot_user_error"),
                    self.client.user.avatar.url,
                )
            )
        elif user == interaction.user:
            return await interaction.response.send_message(
                embed=construct_error_self_choose_embed(
                    get_msg_from_locale_by_key(
                        interaction.guild.id, "self_choose_error"
                    ),
                    self.client.user.avatar.url,
                )
            )
        elif money > 0 and isinstance(money, int):
            balance = get_user_balance(interaction.guild.id, interaction.user.id)
            if balance < money:
                msg = get_msg_from_locale_by_key(interaction.guild.id, "on_balance")
                return await interaction.response.send_message(
                    embed=construct_error_not_enough_embed(
                        get_msg_from_locale_by_key(
                            interaction.guild.id, "not_enough_money_error"
                        ),
                        interaction.user.display_avatar,
                        f"{msg} {balance}",
                    )
                )
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
                        interaction.guild.id,
                    )
                )
        else:
            return await interaction.response.send_message(
                embed=construct_error_negative_value_embed(
                    get_msg_from_locale_by_key(
                        interaction.guild.id, "negative_value_error"
                    ),
                    self.client.user.avatar.url,
                    money,
                )
            )

    @nextcord.slash_command(
        name="add-shop",
        description="Add role to shop",
        name_localizations=get_localized_name("add-shop"),
        description_localizations=get_localized_description("add-shop"),
        default_member_permissions=Permissions(administrator=True),
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
            description_localizations={
                "ru": "Количество денег, которое должна стоить роль"
            },
        ),
    ):
        if cost < 0:
            return await interaction.response.send_message(
                embed=construct_error_negative_value_embed(
                    get_msg_from_locale_by_key(
                        interaction.guild.id, "negative_value_error"
                    ),
                    self.client.user.avatar.url,
                    cost,
                )
            )
        if is_role_in_shop(interaction.guild.id, role.id) is True:
            embed = nextcord.Embed(
                title="error",
                description=get_msg_from_locale_by_key(
                    interaction.guild.id, "already_in_shop"
                ),
                color=DEFAULT_BOT_COLOR,
            )
            return await interaction.response.send_message(embed=embed)
        guild_roles = parse_server_roles(interaction.guild)
        if len(guild_roles) >= 25:
            embed = nextcord.Embed(
                title="error",
                description=get_msg_from_locale_by_key(
                    interaction.guild.id, "too_many_roles"
                ),
                color=DEFAULT_BOT_COLOR,
            )
            return await interaction.response.send_message(embed=embed)
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
                interaction.guild.id,
            )
        )

    @nextcord.slash_command(
        name="remove-shop",
        description="Remove role from shop",
        name_localizations=get_localized_name("remove-shop"),
        description_localizations=get_localized_description("remove-shop"),
        default_member_permissions=Permissions(administrator=True),
    )
    @application_checks.has_permissions(manage_guild=True)
    async def __remove_shop(
        self,
        interaction: Interaction,
        role: Optional[nextcord.Role] = SlashOption(
            required=True,
            description="Discord role on your server",
            description_localizations={"ru": "Дискордовская роль на вашем сервере"},
        ),
    ):
        if is_role_in_shop(interaction.guild.id, role.id) is False:
            embed = nextcord.Embed(
                title="error",
                description=get_msg_from_locale_by_key(
                    interaction.guild.id, "not_in_shop"
                ),
                color=DEFAULT_BOT_COLOR,
            )
            return await interaction.response.send_message(embed=embed)
        delete_role_from_shop(interaction.guild.id, role)
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
                interaction.guild.id,
            )
        )

    @nextcord.slash_command(
        name="shop",
        description="show role shop menu",
        name_localizations=get_localized_name("shop"),
        description_localizations=get_localized_description("shop"),
        default_member_permissions=Permissions(send_messages=True),
    )
    async def __shop(self, interaction: Interaction):
        guild_roles = parse_server_roles(interaction.guild)
        pages = SelectButtonMenuPages(
            source=MyEmbedDescriptionPageSource(guild_roles, interaction.guild.id),
            guild=interaction.guild,
            disabled=False,
        )
        await pages.start(interaction=interaction)

    @nextcord.slash_command(
        name="add-custom-shop",
        description="add custom role to shop",
        name_localizations=get_localized_name("add-custom-shop"),
        description_localizations=get_localized_description("add-custom-shop"),
        default_member_permissions=Permissions(send_messages=True),
        guild_ids=[1006113954331885648],
    )
    async def __add_custom_shop(
        self,
        interaction: Interaction,
        role_name: Optional[str] = SlashOption(
            required=True,
            description="Discord role on your server",
            description_localizations={"ru": "Дискордовская роль на вашем сервере"},
        ),
        cost: Optional[int] = SlashOption(
            required=True,
            description="Number of money role will cost",
            description_localizations={
                "ru": "Количество денег, которое должна стоить роль"
            },
        ),
    ):
        balance = get_user_balance(interaction.guild.id, interaction.user.id)
        if balance >= config.settings["default_custom_shop_create_role"]:
            if 100000 > cost > 100:
                if nextcord.utils.get(interaction.guild.roles, name=role_name) is None:
                    colors = {
                        "Белый": 0xFFFAFA,
                        "Чёрный": 0x000000,
                        "Голубой": 0x00BFFF,
                        "Синий": 0x0000FF,
                        "Зеленый": 0x008000,
                        "Салатовый": 0x32CD32,
                        "Фиолетовый": 0x800080,
                        "Розовый": 0xFF69B4,
                        "Красный": 0xFF0000,
                        "Жёлтый": 0xFFFF00,
                        "Персиковый": 0xFFDAB9,
                        "Золотой": 0xFFD700,
                        "Циановый": 0x00FFFF,
                        "Оранжевый": 0xFFA500,
                        "Аквамарин": 0x7FFFD4,
                        "Светлый-Циан": 0xE0FFFF,
                        "Жёлто-Зеленый": 0xADFF2F,
                        "Летний-Зеленый": 0x00FF7F,
                        "Морской-Голубой": 0x20B2AA,
                        "Тёмная-Орхидея": 0x9932CC,
                        "Светло-Розовый": 0xFFB6C1,
                        "Серый": 0x808080,
                        "Тёмно-серый": 0x696969,
                    }

                    view_color_change = nextcord.ui.View()
                    select = nextcord.ui.Select()
                    for color in colors:
                        select.add_option(label=color)

                    async def color_callback(
                        inter: Interaction,
                    ) -> Coroutine[Any, Any, None]:
                        if inter.user == interaction.user:
                            await inter.response.defer()
                            await inter.delete_original_message()
                            if get_custom_shop_roles_limit(inter.guild.id):
                                return await inter.send(
                                    "В магазине достигнут лимит ролей - 50!",
                                    delete_after=5,
                                )

                            await inter.guild.create_role(
                                name=role_name,
                                color=nextcord.Colour(colors[select.values[0]]),
                            )

                            role = nextcord.utils.get(inter.guild.roles, name=role_name)
                            write_role_in_custom_shop(
                                inter.guild.id, role, cost, inter.user.id
                            )
                            await inter.user.add_roles(role)
                            await inter.send("Роль была создана!", delete_after=5)
                        else:
                            await inter.response.defer()

                    select.callback = color_callback
                    view_color_change.add_item(select)
                    await interaction.send(
                        content="Выберите цвет", view=view_color_change
                    )
                else:
                    await interaction.send(
                        f"**{interaction.user.mention}**, роль с таким название уже существует"
                    )
            else:
                await interaction.send(
                    "Роль должна стоить не более 100000 и не менее 100"
                )
        else:
            await interaction.send(
                f"**{interaction.user.mention}**, у вас не хватает денег. Нужно 1000"
            )

    @nextcord.slash_command(
        name="custom-shop",
        description="custom roles shop",
        name_localizations=get_localized_name("custom-shop"),
        description_localizations=get_localized_description("custom-shop"),
        default_member_permissions=Permissions(send_messages=True),
        guild_ids=[1006113954331885648],
    )
    async def __custom_shop(self, interaction: Interaction):
        # await interaction.send("Загружаем магазин...")
        embed, view = await custom_shop_embed(
            inter=interaction, pagen=1, order="notnew"
        )
        await interaction.response.send_message(embed=embed, view=view)

    @nextcord.slash_command(
        name="income",
        name_localizations=get_localized_name("income"),
        description_localizations=get_localized_description("income"),
        default_member_permissions=Permissions(administrator=True),
    )
    @application_checks.has_permissions(manage_guild=True)
    async def __income(self, interaction: Interaction):
        """
        This is the set slash command that will be the prefix of income commands.
        """
        pass

    @__income.subcommand(
        name="role_add",
        description="Add role to income and users with role will get money per 12 hours",
        name_localizations=get_localized_name("income_role_add"),
        description_localizations=get_localized_description("income_role_add"),
    )
    async def __income_role_add(
        self,
        interaction: Interaction,
        role: Optional[nextcord.Role] = SlashOption(
            required=True,
            description="Discord role on your server",
            description_localizations={"ru": "Дискордовская роль на вашем сервере"},
        ),
        income: Optional[int] = SlashOption(
            required=True,
            description="Number of money role will cost",
            description_localizations={
                "ru": "Количество денег, которое будут получать пользователи с данной ролью"
            },
        ),
    ):
        if income <= 0:
            return await interaction.response.send_message(
                embed=construct_error_negative_value_embed(
                    get_msg_from_locale_by_key(
                        interaction.guild.id, "negative_value_error"
                    ),
                    self.client.user.avatar.url,
                    cost,
                )
            )
        if is_role_in_income(interaction.guild.id, role.id) is True:
            embed = nextcord.Embed(
                title="error",
                description=get_msg_from_locale_by_key(
                    interaction.guild.id, "already_in_income"
                ),
                color=DEFAULT_BOT_COLOR,
            )
            return await interaction.response.send_message(embed=embed)
        write_role_in_income(interaction.guild.id, role, income)
        message = get_msg_from_locale_by_key(
            interaction.guild.id, f"income_{interaction.application_command.name}"
        )
        requested = get_msg_from_locale_by_key(interaction.guild.id, "requested_by")
        currency_symbol = get_guild_currency_symbol(interaction.guild.id)
        await interaction.response.send_message(
            embed=construct_basic_embed(
                interaction.application_command.name,
                f"{role.mention} {message} **{income}** {currency_symbol}",
                f"{requested} {interaction.user}",
                interaction.user.display_avatar,
                interaction.guild.id,
            )
        )

    @__income.subcommand(
        name="role_remove",
        description="Choose bot's respond's main language on your server!",
        name_localizations=get_localized_name("income_role_remove"),
        description_localizations=get_localized_description("income_role_remove"),
    )
    async def __income_role_remove(
        self,
        interaction: Interaction,
        role: Optional[nextcord.Role] = SlashOption(
            required=True,
            description="Discord role on your server",
            description_localizations={"ru": "Дискордовская роль на вашем сервере"},
        ),
    ):
        if is_role_in_income(interaction.guild.id, role.id) is False:
            embed = nextcord.Embed(
                title="error",
                description=get_msg_from_locale_by_key(
                    interaction.guild.id, "not_in_income"
                ),
                color=DEFAULT_BOT_COLOR,
            )
            return await interaction.response.send_message(embed=embed)
        delete_role_from_income(interaction.guild.id, role)
        requested = get_msg_from_locale_by_key(interaction.guild.id, "requested_by")
        message = get_msg_from_locale_by_key(
            interaction.guild.id, f"income_{interaction.application_command.name}"
        )
        await interaction.response.send_message(
            embed=construct_basic_embed(
                interaction.application_command.name,
                f"{role.mention} {message}",
                f"{requested} {interaction.user}",
                interaction.user.display_avatar,
                interaction.guild.id,
            )
        )

    @__income.subcommand(
        name="channel",
        description="Turn on/Turn off income in indicated channel",
        name_localizations=get_localized_name("income_channel"),
        description_localizations=get_localized_description("income_channel"),
    )
    async def __income_channel_add(
        self,
        interaction: Interaction,
        channel: Optional[GuildChannel] = SlashOption(
            required=True,
            description="Discord channel on your server",
            description_localizations={"ru": "Дискордовский канал на вашем сервере"},
        ),
        enabled: Optional[bool] = SlashOption(
            required=True,
            description="True - turn on, False - Turn off",
            name_localizations={"ru": "включено"},
            description_localizations={"ru": "True - включить, False - выключить"},
        ),
    ):
        write_channel_in_config(interaction.guild.id, channel.id, enabled)
        message = get_msg_from_locale_by_key(
            interaction.guild.id, f"income_{interaction.application_command.name}"
        )
        message_2 = get_msg_from_locale_by_key(
            interaction.guild.id, f"income_{interaction.application_command.name}_2"
        )
        requested = get_msg_from_locale_by_key(interaction.guild.id, "requested_by")
        if enabled is True:
            enabled = get_msg_from_locale_by_key(interaction.guild.id, "enabled")
        else:
            enabled = get_msg_from_locale_by_key(interaction.guild.id, "disabled")
        await interaction.response.send_message(
            embed=construct_basic_embed(
                interaction.application_command.name,
                f"{message} {channel.mention} {message_2} **{enabled}**",
                f"{requested} {interaction.user}",
                interaction.user.display_avatar,
                interaction.guild.id,
            )
        )

    @__income.subcommand(
        name="min_max_message",
        description="Set min and max income for writing messages",
        name_localizations=get_localized_name("income_min_max_message"),
        description_localizations=get_localized_description("income_min_max_message"),
    )
    async def __min_max_message_income(
        self,
        interaction: Interaction,
        min_msg_income: Optional[int] = SlashOption(
            required=True,
            description="Minimal income for writing messages",
            description_localizations={
                "ru": "Минимальный доход за написание сообщений"
            },
        ),
        max_msg_income: Optional[int] = SlashOption(
            required=True,
            description="Maximal income for writing messages",
            description_localizations={
                "ru": "Максимальный доход за написание сообщений"
            },
        ),
    ):
        if min_msg_income < 0 or max_msg_income < 0:
            return await interaction.response.send_message(
                embed=construct_error_negative_value_embed(
                    get_msg_from_locale_by_key(
                        interaction.guild.id, "negative_value_error"
                    ),
                    self.client.user.avatar.url,
                    f"{min_msg_income} - {max_msg_income}",
                )
            )
        if max_msg_income < min_msg_income:
            return
        update_guild_min_max_msg_income(
            interaction.guild.id, min_msg_income, max_msg_income
        )
        message = get_msg_from_locale_by_key(
            interaction.guild.id, f"income_{interaction.application_command.name}"
        )
        requested = get_msg_from_locale_by_key(interaction.guild.id, "requested_by")
        await interaction.response.send_message(
            embed=construct_basic_embed(
                interaction.application_command.name,
                f"{message} **{min_msg_income}** - **{max_msg_income}**",
                f"{requested} {interaction.user}",
                interaction.user.display_avatar,
                interaction.guild.id,
            )
        )

    @__income.subcommand(
        name="min_max_voice",
        description="Set min and max income for being in voice chat",
        name_localizations=get_localized_name("income_min_max_voice"),
        description_localizations=get_localized_description("income_min_max_voice"),
    )
    async def __min_max_voice_income(
        self,
        interaction: Interaction,
        min_voice_income: Optional[int] = SlashOption(
            required=True,
            description="Maximal income for being in voice",
            description_localizations={
                "ru": "Минимальный доход за нахождение в голосовом чате"
            },
        ),
        max_voice_income: Optional[int] = SlashOption(
            required=True,
            description="Maximal income for being in voice",
            description_localizations={
                "ru": "Максимальный доход за нахождение в голосовом чате"
            },
        ),
    ):
        if min_voice_income < 0 or max_voice_income < 0:
            return await interaction.response.send_message(
                embed=construct_error_negative_value_embed(
                    get_msg_from_locale_by_key(
                        interaction.guild.id, "negative_value_error"
                    ),
                    self.client.user.avatar.url,
                    f"{min_voice_income} - {max_voice_income}",
                )
            )
        if max_voice_income < min_voice_income:
            return await interaction.response.send_message(
                embed=construct_error_negative_value_embed(
                    get_msg_from_locale_by_key(
                        interaction.guild.id, "negative_value_error"
                    ),
                    self.client.user.avatar.url,
                    f"{min_voice_income} - {max_voice_income}",
                )
            )
        update_guild_min_max_voice_income(
            interaction.guild.id, min_voice_income, max_voice_income
        )
        message = get_msg_from_locale_by_key(
            interaction.guild.id, f"income_{interaction.application_command.name}"
        )
        requested = get_msg_from_locale_by_key(interaction.guild.id, "requested_by")
        await interaction.response.send_message(
            embed=construct_basic_embed(
                interaction.application_command.name,
                f"{message} **{min_voice_income}** - **{max_voice_income}**",
                f"{requested} {interaction.user}",
                interaction.user.display_avatar,
                interaction.guild.id,
            )
        )

    @__income.subcommand(
        name="messages_per_income",
        description="Set messages users must write before getting income",
        name_localizations=get_localized_name("income_messages_per_income"),
        description_localizations=get_localized_description(
            "income_messages_per_income"
        ),
    )
    async def __messages_per_income(
        self,
        interaction: Interaction,
        msg_per_income: Optional[int] = SlashOption(
            required=True,
            description="Messages user must write for income",
            description_localizations={"ru": "Cообщений нужно написать для дохода"},
        ),
    ):
        if msg_per_income < 1:
            return await interaction.response.send_message(
                embed=construct_error_negative_value_embed(
                    get_msg_from_locale_by_key(
                        interaction.guild.id, "negative_value_error"
                    ),
                    self.client.user.avatar.url,
                    f"{min_msg_income} - {max_msg_income}",
                )
            )
        update_guild_msg_cooldown(interaction.guild.id, msg_per_income)
        message = get_msg_from_locale_by_key(
            interaction.guild.id, f"income_{interaction.application_command.name}"
        )
        requested = get_msg_from_locale_by_key(interaction.guild.id, "requested_by")
        await interaction.response.send_message(
            embed=construct_basic_embed(
                interaction.application_command.name,
                f"{message} **{msg_per_income}**",
                f"{requested} {interaction.user}",
                interaction.user.display_avatar,
                interaction.guild.id,
            )
        )

    @__income.subcommand(
        name="voice_minutes",
        description="Set minutes users must spent in voice chat before income",
        name_localizations=get_localized_name("income_voice_minutes"),
        description_localizations=get_localized_description("income_voice_minutes"),
    )
    async def __voice_minutes_income(
        self,
        interaction: Interaction,
        voice_minutes: Optional[int] = SlashOption(
            required=True,
            description="Minutes user must be in voice channel",
            description_localizations={"ru": "Минут нужно быть в голосовом канале"},
        ),
    ):
        if voice_minutes < 1:
            return await interaction.response.send_message(
                embed=construct_error_negative_value_embed(
                    get_msg_from_locale_by_key(
                        interaction.guild.id, "negative_value_error"
                    ),
                    self.client.user.avatar.url,
                    f"{min_msg_income} - {max_msg_income}",
                )
            )
        update_guild_voice_minutes_for_money(interaction.guild.id, voice_minutes)
        message = get_msg_from_locale_by_key(
            interaction.guild.id, f"income_{interaction.application_command.name}"
        )
        requested = get_msg_from_locale_by_key(interaction.guild.id, "requested_by")
        await interaction.response.send_message(
            embed=construct_basic_embed(
                interaction.application_command.name,
                f"{message} **{voice_minutes}**",
                f"{requested} {interaction.user}",
                interaction.user.display_avatar,
                interaction.guild.id,
            )
        )

    @__income.subcommand(
        name="display_roles",
        description="Show list of roles with income set",
        name_localizations=get_localized_name("income_display_roles"),
        description_localizations=get_localized_description("income_display_roles"),
    )
    async def __income_display_roles(self, interaction: Interaction):
        roles = list_income_roles(interaction.guild.id)
        source_for_pages = []
        for row in roles:
            role = nextcord.utils.get(interaction.guild.roles, id=row[0])
            role = role.mention
            income_msg = localize_name(interaction.guild.id, "income").capitalize()
            level = f"{income_msg} - {row[1]}"
            source_for_pages.append([level, role])
        pages = NoStopButtonMenuPages(
            source=AutorolesList(source_for_pages, interaction.guild.id),
        )
        await pages.start(interaction=interaction)


def setup(client):
    client.add_cog(Economics(client))
