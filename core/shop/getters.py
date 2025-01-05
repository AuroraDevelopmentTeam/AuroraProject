import nextcord
from nextcord import Interaction
from nextcord.ui import Button, Select, View

from core.db_utils import fetch_one, fetch_all
from core.shop.updaters import buy_role, delete_role_from_shop
import sqlite3
from typing import Coroutine, Any
from core.dataclassesList import CustomRole
from core.money.getters import get_guild_currency_symbol


class BuyButton(Button):
    def __init__(
            self, label, interaction, role, emoji=None
    ):  # TODO make custom shop emojis for guilds
        super().__init__(label=label, style=nextcord.ButtonStyle.primary, emoji="🛒")
        self.interaction = interaction
        self.role = role

    async def callback(self, interaction) -> None:
        if interaction.user == self.interaction.user:

            await interaction.response.defer()
            role = nextcord.utils.get(self.interaction.guild.roles, name=self.role)
            await buy_role(self.interaction, role)
        else:
            await interaction.response.defer()


class NextPageButton(Button):
    def __init__(
            self, label, interaction, page, emoji=None, shop_filter="notnew"
    ):  # filt = filter
        super().__init__(style=nextcord.ButtonStyle.secondary, emoji=emoji, row=3)
        self.interaction = interaction
        self.page: int = page
        self.shop_filter: str = shop_filter

    async def callback(self, interaction) -> Coroutine[Any, Any, None]:
        if interaction.user == self.interaction.user:

            await interaction.response.defer()
            # await interaction.delete_original_message()
            # await interaction.edit_original_message(embed=None,view=None,content=None)
            embed, view = await custom_shop_embed(
                inter=self.interaction, pagen=self.page, order=self.shop_filter
            )
            await self.interaction.edit_original_message(embed=embed, view=view)
        else:
            await interaction.response.defer()


class ShopLeave(Button):
    def __init__(self):
        super().__init__(style=nextcord.ButtonStyle.secondary, emoji="🇽", row=3)

    async def callback(self, interaction) -> None:
        await interaction.response.defer()
        await interaction.delete_original_message()


async def get_custom_shop_roles_limit(
        guild_id: int,
) -> bool:  # TODO сделать чтобы создатель сервера мог регулировать лимит и переименовать, а то не совсем соответствует
    roles = await fetch_all(
        "SELECT * FROM custom_shop WHERE guild_id = %s", (guild_id,)
    )
    if len(roles) >= 60:  # в будущем можно будет увеличить
        return True
    return False


async def custom_shop_embed(
        inter: Interaction, pagen: int = 1, order: str = "notnew"
) -> Coroutine[Any, Any, tuple[nextcord.Embed, View]]:
    embed = nextcord.Embed(title="Магазин личных ролей")
    view = View()
    notnew, new, highcost, lowcost = False, False, False, False
    if order == "notnew":
        roles = await fetch_all(
            f"SELECT * FROM custom_shop WHERE guild_id = {inter.guild.id} ORDER BY created ASC"
        )
        notnew = True
    elif order == "new":
        roles = await fetch_all(
            f"SELECT * FROM custom_shop WHERE guild_id = {inter.guild.id} ORDER BY created DESC"
        )
        new = True
    elif order == "highcost":
        roles = await fetch_all(
            f"SELECT * FROM custom_shop WHERE guild_id = {inter.guild.id} ORDER BY cost DESC"
        )
        highcost = True
    elif order == "lowcost":
        roles = await fetch_all(
            f"SELECT * FROM custom_shop WHERE guild_id = {inter.guild.id} ORDER BY cost ASC"
        )
        lowcost = True
    roles = list(roles)
    pagescol = len(roles) // 5
    if len(roles) % 5 != 0:
        pagescol += 1
    x = pagen * 5
    col = x - 5
    currency_symbol = await get_guild_currency_symbol(inter.guild.id)
    for each in roles[x - 5: x]:
        each = CustomRole(*list(each))
        col += 1
        objecta = nextcord.utils.get(inter.guild.roles, id=each.role_id)
        if objecta is None:
            await delete_role_from_shop(inter.guild, each.role_id)
            return await custom_shop_embed(inter, pagen, order)
        button = BuyButton(label=col, interaction=inter, role=objecta.name)
        view.add_item(button)
        embed.add_field(
            name=f" ⁣ ",
            value=f"**{col}) {objecta.mention} \n Продавец: {inter.client.get_user(each.owner_id).mention} \n \
            Цена: {each.cost} {currency_symbol} \n Куплена раз: {each.bought}**",
            inline=False,
        )
    embed.set_footer(text=f"Страница {pagen} из {str(pagescol)}")
    embed.set_thumbnail(url=inter.user.avatar.url)
    select = Select(
        options=[
            nextcord.SelectOption(label="Сначала старые", default=notnew),
            nextcord.SelectOption(label="Сначала новые", default=new),
            nextcord.SelectOption(label="Сначала дорогие", default=highcost),
            nextcord.SelectOption(label="Сначала дешевые", default=lowcost),
        ]
    )

    async def select_callback(interaction):
        if inter.user == interaction.user:

            await interaction.response.defer()
            # await interaction.delete_original_message()
            if select.values[0] == "Сначала старые":
                gay, sex = await custom_shop_embed(inter=inter, order="notnew")
                await inter.edit_original_message(embed=gay, view=sex)
            if select.values[0] == "Сначала новые":
                gay, sex = await custom_shop_embed(inter=inter, order="new")
                await inter.edit_original_message(embed=gay, view=sex)
            if select.values[0] == "Сначала дорогие":
                gay, sex = await custom_shop_embed(inter=inter, order="highcost")
                await inter.edit_original_message(embed=gay, view=sex)
            if select.values[0] == "Сначала дешевые":
                gay, sex = await custom_shop_embed(inter=inter, order="lowcost")
                await inter.edit_original_message(embed=gay, view=sex)
        else:
            await interaction.response.defer()

    select.callback = select_callback
    view.add_item(select)
    button1 = NextPageButton(
        label=f"Страница {pagen - 1}",
        interaction=inter,
        page=pagen - 1,
        emoji="⬅️",
        shop_filter=order,
    )
    button3 = NextPageButton(
        label=f"Страница {pagen + 1}",
        interaction=inter,
        page=pagen + 1,
        emoji="➡️",
        shop_filter=order,
    )
    button2 = ShopLeave()
    if pagen >= 2:
        pass
    else:
        button1.disabled = True
        button3.disabled = True
    if pagen < pagescol:
        button3.disabled = False
    else:
        button3.disabled = True
    view.add_item(button1)
    view.add_item(button2)
    view.add_item(button3)
    return embed, view


async def get_custom_shop_enabled(guild_id: int) -> bool:
    enabled = await fetch_one(
        f"SELECT enabled FROM custom_shop_config WHERE guild_id = {guild_id}"
    )
    return bool(int(enabled[0]))


async def get_custom_shop_role_create_cost(guild_id: int) -> int:
    role_create_cost = cursor.execute(
        f"role_create_cost FROM custom_shop_config WHERE guild_id = {guild_id}"
    )
    return role_create_cost[0]
