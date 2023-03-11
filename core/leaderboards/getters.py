import nextcord
from nextcord import Interaction
from nextcord.ui import Button, Select, View
import sqlite3
from typing import Coroutine, Any
from core.embeds import construct_top_embed
from core.utils import format_seconds_to_hhmmss

gifs = {
    "messages": "https://i.pinimg.com/originals/b0/f6/64/b0f6645a029e85c67efb91c7c750ba0b.gif", 
    "balance": "https://cdn.discordapp.com/attachments/772385814483173398/1002913553373732945/a6d84a1408a1e5a2.gif",
    "voice": "https://giffiles.alphacoders.com/209/209343.gif",
    "waifu": "https://media.discordapp.net/attachments/525436099200417792/880565982953873448/ezgif-7-14708239185a.gif",
    "levels": "https://i.pinimg.com/originals/73/b8/91/73b891095024146aa50ba703f1312a38.gif",
}

class NextPageButton(Button):
    def __init__(
        self, label, interaction, page, emoji=None, top_filter="balance"
    ):  # filt = filter
        super().__init__(style=nextcord.ButtonStyle.secondary, emoji=emoji, row=3)
        self.interaction = interaction
        self.page: int = page
        self.top_filter: str = top_filter

    async def callback(self, interaction) -> Coroutine[Any, Any, None]:
        if interaction.user == self.interaction.user:

            await interaction.response.defer()
            # await interaction.delete_original_message()
            # await interaction.edit_original_message(embed=None,view=None,content=None)
            embed, view = await custom_top_embed(
                inter=self.interaction, pagen=self.page, order=self.top_filter
            )
            await self.interaction.edit_original_message(embed=embed, view=view)
        else:
            await interaction.response.defer()


class TopLeave(Button):
    def __init__(self):
        super().__init__(style=nextcord.ButtonStyle.secondary, emoji="🇽", row=3)

    async def callback(self, interaction) -> None:
        await interaction.response.defer()
        await interaction.delete_original_message()



async def custom_top_embed(
    inter: Interaction, pagen: int = 1, order: str = "balance"
) -> tuple[nextcord.Embed, View]:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    embed = nextcord.Embed(title=f"Топ по {order}")
    view = View()
    balance, voice, waifu, messages, levels = False, False, False, False, False
    currency = ""
    if order == "balance":
        currency = ":dollar:"
        roles = cursor.execute(
            f"SELECT user_id, balance FROM money WHERE guild_id = {inter.guild.id} ORDER BY balance DESC"
        ).fetchall()
        balance = True
    elif order == "voice":
        roles = cursor.execute(
            f"SELECT user_id, in_voice FROM stats WHERE guild_id = {inter.guild.id} ORDER BY in_voice DESC"
        ).fetchall()
        voice = True
    elif order == "waifu":
        roles = cursor.execute(
            f"SELECT user_id, gift_price FROM gifts WHERE guild_id = {inter.guild.id} ORDER BY gift_price DESC"
        ).fetchall()
        waifu = True
    elif order == "messages":
        roles = cursor.execute(
            f"SELECT user_id, messages FROM stats WHERE guild_id = {inter.guild.id} ORDER BY messages DESC"
        ).fetchall()
        messages = True
    elif order == "levels":
        roles = cursor.execute(
            f"SELECT user_id, level FROM levels WHERE guild_id = {inter.guild.id} ORDER BY level DESC"
        ).fetchall()
        levels = True


    cursor.close()
    db.close()
    roles = list(roles)
    pagescol = len(roles) // 5
    if len(roles) % 5 != 0:
        pagescol += 1
    x = pagen * 5
    col = x - 5
    users = []
    for each in roles[x - 5 : x]:
        each = list(each)
        col += 1
        if (user := inter.client.get_user(each[0])) == None: 
            user = await inter.client.fetch_user(each[0])
        if order == "voice":
            each[1] = format_seconds_to_hhmmss(each[1])
        users.append([user, each[1]])
    select = Select(
        options=[
            nextcord.SelectOption(label="Balance", default=balance),
            nextcord.SelectOption(label="Voice", default=voice),
            nextcord.SelectOption(label="Waifu", default=waifu),
            nextcord.SelectOption(label="Messages", default=messages),
            nextcord.SelectOption(label="Levels", default=levels)
        ]
    )

    async def select_callback(interaction):
        if inter.user == interaction.user:

            await interaction.response.defer()
            # await interaction.delete_original_message()
            if select.values[0] == "Balance":
                gay, sex = await custom_top_embed(inter=inter, order="balance")
                await inter.edit_original_message(embed=gay, view=sex)
            if select.values[0] == "Voice":
                gay, sex = await custom_top_embed(inter=inter, order="voice")
                await inter.edit_original_message(embed=gay, view=sex)
            if select.values[0] == "Waifu":
                gay, sex = await custom_top_embed(inter=inter, order="waifu")
                await inter.edit_original_message(embed=gay, view=sex)
            if select.values[0] == "Messages":
                gay, sex = await custom_top_embed(inter=inter, order="messages")
                await inter.edit_original_message(embed=gay, view=sex)
            if select.values[0] == "Levels":
                gay, sex = await custom_top_embed(inter=inter, order="levels")
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
        top_filter=order,
    )
    button3 = NextPageButton(
        label=f"Страница {pagen + 1}",
        interaction=inter,
        page=pagen + 1,
        emoji="➡️",
        top_filter=order,
    )
    button2 = TopLeave()
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
    embed = construct_top_embed(
            inter.application_command.name,
            users,
            f"Страница {pagen} из {str(pagescol)}",
            inter.user.display_avatar,
            currency,
    )
    embed.set_image(url=gifs[order])
    embed.set_thumbnail(url=inter.user.avatar.url)
    return embed, view

