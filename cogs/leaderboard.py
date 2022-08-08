import sqlite3

import nextcord
from nextcord.ext import commands
from nextcord import Interaction, Permissions
from core.embeds import construct_top_embed
from core.money.getters import get_guild_currency_symbol
from core.locales.getters import get_msg_from_locale_by_key, get_localized_name, get_localized_description
from core.utils import format_seconds_to_hhmmss


class Leaderboard(commands.Cog):
    def __init__(self, client):
        self.client = client

    @nextcord.slash_command(
        name="leaderboard",
        description="Leaderboard slash command that will be the prefix of leaderboard commands.",
        name_localizations=get_localized_name("leaderboard"),
        description_localizations=get_localized_description("leaderboard"),
        default_member_permissions=Permissions(send_messages=True)
    )
    async def __leaderboard(self, interaction: Interaction):
        """
        This is the set slash command that will be the prefix of leaderboard commands.
        """
        pass

    @__leaderboard.subcommand(
        name="money", description="money leaderboard on your guild",
        name_localizations=get_localized_name("leaderboard_money"),
        description_localizations=get_localized_description("leaderboard_money")
    )
    async def __money_leaderboard(self, interaction: Interaction):
        await interaction.response.defer()
        db = sqlite3.connect("./databases/main.sqlite")
        cursor = db.cursor()
        money = []
        for row in cursor.execute(
                f"SELECT user_id, balance FROM money WHERE guild_id = {interaction.guild.id} ORDER BY balance DESC LIMIT 18"
        ):
            user = await self.client.fetch_user(row[0])
            money.append([user.mention, row[1]])
        cursor.close()
        db.close()
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
        await interaction.followup.send(embed=embed)

    @__leaderboard.subcommand(
        name="level", description="level leaderboard on your guild",
        name_localizations=get_localized_name("leaderboard_level"),
        description_localizations=get_localized_description("leaderboard_level")
    )
    async def __level_leaderboard(self, interaction: Interaction):
        await interaction.response.defer()
        db = sqlite3.connect("./databases/main.sqlite")
        cursor = db.cursor()
        levels = []
        for row in cursor.execute(
                f"SELECT user_id, level FROM levels WHERE guild_id = {interaction.guild.id} ORDER BY level DESC LIMIT 18"
        ):
            user = await self.client.fetch_user(row[0])
            levels.append([user.mention, row[1]])
        cursor.close()
        db.close()
        requested = get_msg_from_locale_by_key(interaction.guild.id, "requested_by")
        embed = construct_top_embed(
            interaction.application_command.name,
            levels,
            f"{requested} {interaction.user}",
            interaction.user.display_avatar,
        )
        embed.set_image(
            "https://i.pinimg.com/originals/73/b8/91/73b891095024146aa50ba703f1312a38.gif"
        )
        await interaction.followup.send(embed=embed)

    @__leaderboard.subcommand(name="waifu", description="waifu leaderboard",
                              name_localizations=get_localized_name("leaderboard_waifu"),
                              description_localizations=get_localized_description("leaderboard_waifu"))
    async def __waifu_leaderboard(self, interaction: Interaction):
        await interaction.response.defer()
        db = sqlite3.connect("./databases/main.sqlite")
        cursor = db.cursor()
        levels = []
        for row in cursor.execute(
                f"SELECT user_id, gift_price FROM gifts WHERE guild_id = {interaction.guild.id} ORDER BY gift_price DESC LIMIT 18"
        ):
            user = await self.client.fetch_user(row[0])
            levels.append([user.mention, row[1]])
        cursor.close()
        db.close()
        currency_symbol = get_guild_currency_symbol(interaction.guild.id)
        requested = get_msg_from_locale_by_key(interaction.guild.id, "requested_by")
        embed = construct_top_embed(
            interaction.application_command.name,
            levels,
            f"{requested} {interaction.user}",
            interaction.user.display_avatar,
            currency_symbol,
        )
        embed.set_image(url="https://media.discordapp.net/attachments/525436099200417792/880565982953873448/ezgif-7-14708239185a.gif")
        await interaction.followup.send(embed=embed)

    @__leaderboard.subcommand(name="voice", description="voice leaderboard")
    async def __voice_leaderboard(self, interaction: Interaction):
        await interaction.response.defer()
        db = sqlite3.connect("./databases/main.sqlite")
        cursor = db.cursor()
        levels = []
        for row in cursor.execute(
                f"SELECT user_id, in_voice FROM stats WHERE guild_id = {interaction.guild.id} ORDER BY in_voice DESC LIMIT 18"
        ):
            user = await self.client.fetch_user(row[0])
            levels.append([user.mention, format_seconds_to_hhmmss(row[1])])
        cursor.close()
        db.close()
        requested = get_msg_from_locale_by_key(interaction.guild.id, "requested_by")
        embed = construct_top_embed(
            interaction.application_command.name,
            levels,
            f"{requested} {interaction.user}",
            interaction.user.display_avatar
        )
        embed.set_image(url="https://giffiles.alphacoders.com/209/209343.gif")
        await interaction.followup.send(embed=embed)

    @__leaderboard.subcommand(name="messages", description="messages leaderboard")
    async def __messages_leaderboard(self, interaction: Interaction):
        await interaction.response.defer()
        db = sqlite3.connect("./databases/main.sqlite")
        cursor = db.cursor()
        levels = []
        for row in cursor.execute(
                f"SELECT user_id, messages FROM stats WHERE guild_id = {interaction.guild.id} ORDER BY messages DESC LIMIT 18"
        ):
            user = await self.client.fetch_user(row[0])
            levels.append([user.mention, row[1]])
        cursor.close()
        db.close()
        requested = get_msg_from_locale_by_key(interaction.guild.id, "requested_by")
        embed = construct_top_embed(
            interaction.application_command.name,
            levels,
            f"{requested} {interaction.user}",
            interaction.user.display_avatar
        )
        embed.set_image(url="https://i.pinimg.com/originals/b0/f6/64/b0f6645a029e85c67efb91c7c750ba0b.gif")
        await interaction.followup.send(embed=embed)


def setup(client):
    client.add_cog(Leaderboard(client))
