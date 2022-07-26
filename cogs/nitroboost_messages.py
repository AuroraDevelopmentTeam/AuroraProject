import nextcord
from nextcord.ext import commands
from nextcord import Interaction
from nextcord.ext import menus
from core.ui.paginator import MyEmbedFieldPageSource


class NitroBoostAnnouncement(commands.Cog):
    def __init__(self, client):
        self.client = client

    @nextcord.slash_command(name="menutest", description="oh shit i'm sorry")
    async def __menutest(self, interaction: Interaction):
        fields = [
            ("Black", "#000000"),
            ("Blue", "#0000FF"),
            ("Brown", "#A52A2A"),
            ("Green", "#00FF00"),
            ("Grey", "#808080"),
            ("Orange", "#FFA500"),
            ("Pink", "#FFC0CB"),
            ("Purple", "#800080"),
            ("Red", "#FF0000"),
            ("White", "#FFFFFF"),
            ("Yellow", "#FFFF00"),
        ]
        pages = menus.ButtonMenuPages(
            source=MyEmbedFieldPageSource(fields),
            clear_buttons_after=True,
        )
        await pages.start(interaction=interaction)


def setup(client):
    client.add_cog(NitroBoostAnnouncement(client))
