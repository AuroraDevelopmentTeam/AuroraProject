from nextcord.ext import menus
from nextcord.ext.menus import MenuPaginationButton
import nextcord
from nextcord import Embed, Interaction
from core.embeds import DEFAULT_BOT_COLOR
from core.parsers import parse_server_roles
from core.locales.getters import get_msg_from_locale_by_key
from core.embeds import construct_basic_embed, construct_top_embed, DEFAULT_BOT_COLOR
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
from core.locales.getters import get_msg_from_locale_by_key, localize_name
from core.errors import (
    construct_error_forbidden_embed,
    construct_error_not_enough_embed,
)
from typing import Union
from core.ui.buttons import create_button
from core.emojify import SHOP


class MyEmbedFieldPageSource(menus.ListPageSource):
    def __init__(self, data):
        super().__init__(data, per_page=6)

    async def format_page(self, menu, entries) -> Embed:
        embed = Embed(title="Shop", color=DEFAULT_BOT_COLOR)
        for entry in entries:
            embed.add_field(name=entry[0], value=entry[1], inline=True)
        embed.set_footer(text=f"{menu.current_page + 1}/{self.get_max_pages()}")
        return embed


class Dropdown(nextcord.ui.Select):
    def __init__(self, guild: nextcord.Guild, disabled: bool):
        self.guild = guild
        self.price = []
        self.role_list = []
        roles = parse_server_roles(guild, False)
        msg = get_msg_from_locale_by_key(self.guild.id, "price")
        sel_opt = []
        if len(roles) > 0:
            for i in range(len(roles)):
                self.price.append(roles[i][1])
                self.role_list.append(roles[i][0])
                sel_opt.append(
                    nextcord.SelectOption(
                        label=f"{i + 1}",
                        description=f"@{roles[i][0].name}, \n{msg} {roles[i][1]}",
                    )
                )
            super().__init__(
                placeholder="Select role from shop",
                min_values=1,
                max_values=1,
                options=sel_opt,
                disabled=disabled,
            )
        else:
            sel_opt = [nextcord.SelectOption(label=f"...", description="...")]
            super().__init__(
                placeholder="Select role from shop",
                min_values=1,
                max_values=1,
                options=sel_opt,
                disabled=disabled,
            )

    async def callback(self, interaction: Interaction):
        embed = nextcord.Embed(color=DEFAULT_BOT_COLOR)
        msg = get_msg_from_locale_by_key(self.guild.id, "shop")
        if self.values[0] != "...":
            balance = await get_user_balance(interaction.guild.id, interaction.user.id)
            msg = get_msg_from_locale_by_key(self.guild.id, "on_balance")
            if balance < (self.price[int(self.values[0]) - 1]):
                embed = construct_error_not_enough_embed(
                    get_msg_from_locale_by_key(
                        interaction.guild.id, "not_enough_money_error"
                    ),
                    interaction.user.display_avatar,
                    f"{msg} {balance}",
                )
                return await interaction.message.edit(
                    embed=embed,
                    view=DropdownView(
                        interaction.guild, interaction.user, disabled=True
                    ),
                )
            if self.role_list[int(self.values[0]) - 1] in interaction.user.roles:
                message = get_msg_from_locale_by_key(
                    interaction.guild.id, "already_have"
                )
                embed.add_field(name="error", value=f"{message}")
                return await interaction.message.edit(
                    embed=embed,
                    view=DropdownView(
                        interaction.guild, interaction.user, disabled=True
                    ),
                )
            await interaction.user.add_roles(
                self.role_list[int(self.values[0]) - 1]
            )
            msg = get_msg_from_locale_by_key(self.guild.id, "shop")
            embed.description(f"{msg} {self.role_list[int(self.values[0]) - 1].mention}")
            embed.title(f"{SHOP} {localize_name(self.guild_id, 'shop').capitalize()}")
            await update_user_balance(
                interaction.guild.id,
                interaction.user.id,
                -(self.price[int(self.values[0]) - 1]),
            )
            balance = await get_user_balance(interaction.guild.id, interaction.user.id)
            msg = get_msg_from_locale_by_key(interaction.guild.id, "on_balance")
            embed.set_footer(
                text=f"{msg} {balance}", icon_url=interaction.user.display_avatar
            )
        else:
            embed.add_field(name="Shop", value=f"ヾ( ￣O￣)ツ	")
        await interaction.message.edit(
            embed=embed,
            view=DropdownView(interaction.guild, interaction.user, disabled=True),
        )


class DropdownView(nextcord.ui.View):
    def __init__(
            self,
            guild: nextcord.Guild,
            author: Union[nextcord.Member, nextcord.User],
            disabled: bool,
    ):
        self.guild = guild
        self.author = author
        self.disabled = disabled
        super().__init__()
        self.add_item(Dropdown(guild=self.guild, disabled=disabled))

    async def interaction_check(self, interaction: Interaction) -> bool:
        if interaction.user != self.author:
            return False
        return True


class MyEmbedDescriptionPageSource(menus.ListPageSource):
    def __init__(self, data, guild_id):
        self.guild_id = guild_id
        super().__init__(data, per_page=6)

    async def format_page(self, menu, entries):
        embed = Embed(
            title=f"{SHOP} {localize_name(self.guild_id, 'shop').capitalize()}",
            description="\n".join(entries),
            color=DEFAULT_BOT_COLOR,
        )
        embed.set_image(url="https://64.media.tumblr.com/e9096b8d3440af335d9996455f072ab6"
                            "/tumblr_p5flokH8161qbw2q1o1_1280.gif")
        embed.set_footer(text=f"{menu.current_page + 1}/{self.get_max_pages()}")
        return embed


class SelectButtonMenuPages(menus.ButtonMenuPages, inherit_buttons=False):
    def __init__(
            self,
            source: menus.PageSource,
            guild: nextcord.Guild,
            disabled: bool,
            timeout: int = 60,
    ):
        self.guild = guild
        super().__init__(
            source,
            timeout=timeout,
            disable_buttons_after=True,
            style=nextcord.ButtonStyle.secondary,
        )
        self.add_item(menus.MenuPaginationButton(emoji=self.FIRST_PAGE))
        self.add_item(menus.MenuPaginationButton(emoji=self.PREVIOUS_PAGE))
        self.add_item(menus.MenuPaginationButton(emoji=self.STOP))
        self.add_item(menus.MenuPaginationButton(emoji=self.NEXT_PAGE))
        self.add_item(menus.MenuPaginationButton(emoji=self.LAST_PAGE))
        self.add_item(Dropdown(guild=self.guild, disabled=disabled))


class ShopModal(nextcord.ui.Modal):
    def __init__(self, guild: nextcord.Guild):
        self.guild = guild
        self.guild_roles = []
        self.price = []
        self.role_list = []
        super().__init__("Shop")
        self.number = nextcord.ui.TextInput(
            label="Shop",
            min_length=1,
            max_length=4,
            required=True,
            placeholder="1",
        )
        self.add_item(self.number)

    async def setup_roles(self):
        self.guild_roles = await parse_server_roles(self.guild, False)
        if len(self.guild_roles) > 0:
            for role_info in self.guild_roles:
                self.price.append(role_info[1])
                self.role_list.append(role_info[0])

    async def callback(self, interaction: Interaction):
        if len(self.guild_roles) > 0:
            embed = nextcord.Embed(color=DEFAULT_BOT_COLOR)
            balance = await get_user_balance(interaction.guild.id, interaction.user.id)
            msg = get_msg_from_locale_by_key(self.guild.id, "on_balance")
            if balance < (self.price[int(self.number.value) - 1]):
                embed = construct_error_not_enough_embed(
                    get_msg_from_locale_by_key(
                        interaction.guild.id, "not_enough_money_error"
                    ),
                    interaction.user.display_avatar,
                    f"{msg} {balance}",
                )
                return await interaction.response.send_message(
                    embed=embed)
            if self.role_list[int(self.number.value) - 1] in interaction.user.roles:
                message = get_msg_from_locale_by_key(
                    interaction.guild.id, "already_have"
                )
                embed.add_field(name="error", value=f"{message}")
                return await interaction.response.send_message(
                    embed=embed)
            await interaction.user.add_roles(
                self.role_list[int(self.number.value) - 1]
            )
            msg = get_msg_from_locale_by_key(self.guild.id, "shop")
            embed = nextcord.Embed(color=DEFAULT_BOT_COLOR,
                                   description=f"{msg} {self.role_list[int(self.number.value) - 1].mention}",
                                   title=f"{SHOP} {localize_name(self.guild.id, 'shop').capitalize()}")
            await update_user_balance(
                interaction.guild.id,
                interaction.user.id,
                -(self.price[int(self.number.value) - 1]),
            )
            balance = get_user_balance(interaction.guild.id, interaction.user.id)
            msg = get_msg_from_locale_by_key(interaction.guild.id, "on_balance")
            embed.set_footer(
                text=f"{msg} {balance}", icon_url=interaction.user.display_avatar
            )
            return await interaction.response.send_message(embed=embed)



async def show_modal(interaction: Interaction):
    modal = ShopModal(guild=interaction.guild)
    await modal.setup_roles()
    return await interaction.response.send_modal(modal)


class NewSelectButtonMenuPages(menus.ButtonMenuPages, inherit_buttons=False):
    def __init__(self, source: menus.PageSource, guild_roles: list, interaction: Interaction, timeout: int = 60):
        self.guild_roles = guild_roles
        super().__init__(source, timeout=timeout, disable_buttons_after=True)
        self.add_item(MenuPaginationButton(emoji=self.FIRST_PAGE))
        self.add_item(MenuPaginationButton(emoji=self.PREVIOUS_PAGE))
        self.add_item(create_button(label='🛒', callback=show_modal,
                                    disabled=False))
        self.add_item(MenuPaginationButton(emoji=self.NEXT_PAGE))
        self.add_item(MenuPaginationButton(emoji=self.LAST_PAGE))
        self._disable_unavailable_buttons()


class NewShopView(nextcord.ui.View):
    def __init__(
            self,
            guild: nextcord.Guild,
    ):
        super().__init__(timeout=60)
        self.add_item(MenuPaginationButton(emoji=menus.ButtonMenuPages.FIRST_PAGE, disabled=True))
        self.add_item(MenuPaginationButton(emoji=menus.ButtonMenuPages.PREVIOUS_PAGE, disabled=True))
        self.add_item(create_button(label='🛒', callback=show_modal,
                                    disabled=False))
        self.add_item(MenuPaginationButton(emoji=menus.ButtonMenuPages.NEXT_PAGE, disabled=True))
        self.add_item(MenuPaginationButton(emoji=menus.ButtonMenuPages.LAST_PAGE, disabled=True))
