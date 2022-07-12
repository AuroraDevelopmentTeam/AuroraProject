import nextcord
from nextcord import Interaction
from nextcord.ext import commands
from config import settings
from core.locales import get_msg_from_locale_by_key
from core.embeds import construct_basic_embed


class Information(commands.Cog):

    def __init__(self, client):
        self.client = client

    @nextcord.slash_command(name="ping", description="Sends client's latency in miliseconds")
    async def __ping(self, interaction: Interaction):
        message = get_msg_from_locale_by_key(interaction.guild.id, interaction.application_command.name)
        requested = get_msg_from_locale_by_key(interaction.guild.id, 'requested_by')
        await interaction.response.send_message(
            embed=construct_basic_embed(interaction.application_command.name,
                                        f"{message} {round(self.client.latency * 1000)} ms",
                                        f"{requested} {interaction.user}",
                                        interaction.user.display_avatar))


def setup(client):
    client.add_cog(Information(client))
