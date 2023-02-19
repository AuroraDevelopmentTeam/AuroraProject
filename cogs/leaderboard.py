import sqlite3
from config import settings

import nextcord
from nextcord.ext import commands
from nextcord import Interaction, Permissions
from core.embeds import construct_top_embed
from core.money.getters import get_guild_currency_symbol
from core.locales.getters import (
    get_msg_from_locale_by_key,
    get_localized_name,
    get_localized_description,
)
from core.utils import format_seconds_to_hhmmss

DEFAULT_BOT_COLOR = settings["default_color"]

class LeaderBoardButtons(nextcord.ui.View):
    def __init__(self, client, interaction):
        self.client = client 
        self.interaction = interaction
        super().__init__(timeout=30)
        
        
    async def on_timeout(self):
        for child in self.children:
            child.disabled = True
        message = await self.interaction.original_message()
        await message.edit(view=self)
        
        
    async def interaction_check(self, interaction: nextcord.Interaction) -> bool:
        return interaction.user == self.interaction.user
    
    
    @nextcord.ui.button(label="Баланс")
    async def _balance_top(self, button, interaction):
        db = sqlite3.connect("./databases/main.sqlite")
        cursor = db.cursor()
        money = []
        rows = cursor.execute(
            f"SELECT user_id, balance FROM money WHERE guild_id = {interaction.guild.id} ORDER BY balance DESC LIMIT 18"
        ).fetchall()
        cursor.close()
        db.close()
        for row in rows:
            user = self.client.get_user(row[0])
            if user is None:
                user = await self.client.fetch_user(row[0])
            money.append([user.mention, row[1]])
        currency_symbol = get_guild_currency_symbol(interaction.guild.id)
        requested = get_msg_from_locale_by_key(interaction.guild.id, "requested_by")
        embed = construct_top_embed(
          self.interaction.application_command.name,
          money,
          f"{requested} {interaction.user}",
          interaction.user.display_avatar,
          currency_symbol,
        )
        embed.set_image(
            "https://cdn.discordapp.com/attachments/772385814483173398/1002913553373732945/a6d84a1408a1e5a2.gif"
        )
        embed.set_thumbnail(url=interaction.user.avatar.url)
        await interaction.response.edit_message(embed=embed)
    
    
    @nextcord.ui.button(label="Голосовая активность")
    async def _voice_top(self, button, interaction):
        db = sqlite3.connect("./databases/main.sqlite")
        cursor = db.cursor()
        levels = []
        rows = cursor.execute(
            f"SELECT user_id, in_voice FROM stats WHERE guild_id = {interaction.guild.id} ORDER BY in_voice DESC LIMIT 18"
        ).fetchall()
        cursor.close()
        db.close()
        for row in rows:
            user = self.client.get_user(row[0])
            if user is None:
                user = await self.client.fetch_user(row[0])
            levels.append([user.mention, format_seconds_to_hhmmss(row[1])])
        requested = get_msg_from_locale_by_key(interaction.guild.id, "requested_by")
        embed = construct_top_embed(
            self.interaction.application_command.name,
            levels,
            f"{requested} {interaction.user}",
            interaction.user.display_avatar,
        )
        embed.set_image(url="https://giffiles.alphacoders.com/209/209343.gif")
        embed.set_thumbnail(url=interaction.user.avatar.url)
        await interaction.response.edit_message(embed=embed, view=self)

    @nextcord.ui.button(label="Топ уровни")
    async def _levels_top(self, button, interaction):
        db = sqlite3.connect("./databases/main.sqlite")
        cursor = db.cursor()
        levels = []
        rows = cursor.execute(
            f"SELECT user_id, level FROM levels WHERE guild_id = {interaction.guild.id} ORDER BY level DESC LIMIT 18"
        ).fetchall()
        cursor.close()
        db.close()
        for row in rows:
            user = self.client.get_user(row[0])
            if user is None:
                user = await self.client.fetch_user(row[0])
            levels.append([user.mention, row[1]])
        requested = get_msg_from_locale_by_key(interaction.guild.id, "requested_by")
        embed = construct_top_embed(
            self.interaction.application_command.name,
            levels,
            f"{requested} {interaction.user}",
            interaction.user.display_avatar,
        )
        embed.set_image(
            "https://i.pinimg.com/originals/73/b8/91/73b891095024146aa50ba703f1312a38.gif"
        )
        embed.set_thumbnail(url=interaction.user.avatar.url)
        await interaction.response.edit_message(embed=embed)
        
    @nextcord.ui.button(label="Топ по сообщениям")
    async def _messages_top(self, button, interaction):
        db = sqlite3.connect("./databases/main.sqlite")
        cursor = db.cursor()
        levels = []
        rows = cursor.execute(
            f"SELECT user_id, messages FROM stats WHERE guild_id = {interaction.guild.id} ORDER BY messages DESC LIMIT 18"
        ).fetchall()
        cursor.close()
        db.close()
        for row in rows:
            user = self.client.get_user(row[0])
            if user is None:
                user = await self.client.fetch_user(row[0])
            levels.append([user.mention, row[1]])
        requested = get_msg_from_locale_by_key(interaction.guild.id, "requested_by")
        embed = construct_top_embed(
            self.interaction.application_command.name,
            levels,
            f"{requested} {interaction.user}",
            interaction.user.display_avatar,
        )
        embed.set_image(
            url="https://i.pinimg.com/originals/b0/f6/64/b0f6645a029e85c67efb91c7c750ba0b.gif"
        )
        embed.set_thumbnail(url=interaction.user.avatar.url)
        await interaction.response.edit_message(embed=embed)
    
    @nextcord.ui.button(label="Топ вайфу")
    async def _waifu_top(self, button, interaction):
        db = sqlite3.connect("./databases/main.sqlite")
        cursor = db.cursor()
        levels = []
        rows = cursor.execute(
            f"SELECT user_id, gift_price FROM gifts WHERE guild_id = {interaction.guild.id} ORDER BY gift_price DESC LIMIT 18"
        ).fetchall()
        cursor.close()
        db.close()
        for row in rows:
            user = self.client.get_user(row[0])
            if user is None:
                user = await self.client.fetch_user(row[0])
            levels.append([user.mention, row[1]])
        currency_symbol = get_guild_currency_symbol(interaction.guild.id)
        requested = get_msg_from_locale_by_key(interaction.guild.id, "requested_by")
        embed = construct_top_embed(
            self.interaction.application_command.name,
            levels,
            f"{requested} {interaction.user}",
            interaction.user.display_avatar,
            currency_symbol,
        )
        embed.set_image(
            url="https://media.discordapp.net/attachments/525436099200417792/880565982953873448/ezgif-7-14708239185a.gif"
        )        
        embed.set_thumbnail(url=interaction.user.avatar.url)
        await interaction.response.edit_message(embed=embed)
        
class Leaderboard(commands.Cog):
    def __init__(self, client):
        self.client = client

    @nextcord.slash_command(
        name="leaderboard",
        description="Leaderboard slash command that will be the prefix of leaderboard commands.",
        name_localizations=get_localized_name("leaderboard"),
        guild_ids=[1011711747461238827],
        description_localizations=get_localized_description("leaderboard"),
        default_member_permissions=Permissions(send_messages=True),
    )
    async def _leaderboard(self, interaction: Interaction):
        """
        This is the set slash command that will be the prefix of leaderboard commands.
        """
        
        db = sqlite3.connect("./databases/main.sqlite")
        cursor = db.cursor()
        money = []
        rows = cursor.execute(
            f"SELECT user_id, balance FROM money WHERE guild_id = {interaction.guild.id} ORDER BY balance DESC LIMIT 18"
        ).fetchall()
        cursor.close()
        db.close()
        for row in rows:
            user = self.client.get_user(row[0])
            if user is None:
                user = await self.client.fetch_user(row[0])
            money.append([user.mention, row[1]])
        currency_symbol = get_guild_currency_symbol(interaction.guild.id)
        requested = get_msg_from_locale_by_key(interaction.guild.id, "requested_by")
        embed = construct_top_embed(
          interaction.application_command.name,
          money,
          f"{requested} {interaction.user}",
          interaction.user.display_avatar,
          currency_symbol,
        )
        embed.set_image(
            "https://cdn.discordapp.com/attachments/772385814483173398/1002913553373732945/a6d84a1408a1e5a2.gif"
        )
        embed.set_thumbnail(url=interaction.user.avatar.url)
        await interaction.response.send_message(embed=embed, view=LeaderBoardButtons(self.client, interaction))



def setup(client):
    client.add_cog(Leaderboard(client))
