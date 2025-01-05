import nextcord
from nextcord import Interaction, Permissions
from nextcord.ext import commands

from config import settings
from core.leaderboards.getters import custom_top_embed
from core.locales.getters import (
    get_localized_name,
    get_localized_description,
)

DEFAULT_BOT_COLOR = settings["default_color"]


class Leaderboard(commands.Cog):
    def __init__(self, client):
        self.client = client

    @nextcord.slash_command(
        name="leaderboard",
        description="Leaderboard slash command that will be the prefix of leaderboard commands.",
        name_localizations=get_localized_name("leaderboard"),
        description_localizations=get_localized_description("leaderboard"),
        default_member_permissions=Permissions(send_messages=True),
    )
    async def _leaderboard(self, interaction: Interaction):
        """
        This is the set slash command that will be the prefix of leaderboard commands.
        """
        embed, view = await custom_top_embed(inter=interaction)
        await interaction.send(embed=embed, view=view)


def setup(client):
    client.add_cog(Leaderboard(client))
