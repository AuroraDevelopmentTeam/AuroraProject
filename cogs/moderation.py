import nextcord
from nextcord.ext import commands
from nextcord import Interaction, SlashOption
import datetime
from core.errors import construct_error_forbidden_embed
from core.embeds import construct_basic_embed
from core.locales import get_msg_from_locale_by_key
import humanfriendly
from typing import Optional


class Moderation(commands.Cog):
    def __init__(self, client):
        self.client = client

    @nextcord.slash_command(name="mute", description="Mute with timeout discord's user")
    async def __mute(self, interaction: Interaction, user: Optional[nextcord.Member] = SlashOption(required=True),
                     time: Optional[str] = SlashOption(required=True), *,
                     reason: Optional[str] = SlashOption(required=False)):
        """
        Parameters
        ----------
        interaction: Interaction
            The interaction object
        user: Optional[nextcord.Member]
            The discord's user, tag someone with @
        time: Optional[str]
            Type 1s/1m/1h/1d, this field is the time of mute
        reason: Optional[str]
            This parameter is optional, reason of mute
        """
        try:
            time_in_seconds = humanfriendly.parse_timespan(time)
            requested = get_msg_from_locale_by_key(interaction.guild.id, 'requested_by')
            await user.edit(timeout=nextcord.utils.utcnow() + datetime.timedelta(seconds=time_in_seconds))
            message = get_msg_from_locale_by_key(interaction.guild.id, interaction.application_command.name)
            await interaction.response.send_message(
                embed=construct_basic_embed(interaction.application_command.name,
                                            f"{message} {user.mention}",
                                            f"{requested} {interaction.user}\n📝 {reason}. 🕔 {time}",
                                            interaction.user.display_avatar))
        except nextcord.Forbidden:
            await interaction.response.send_message(
                embed=construct_error_forbidden_embed(
                    get_msg_from_locale_by_key(interaction.guild.id, 'forbidden_error'),
                    self.client.user.avatar.url)
                )


def setup(client):
    client.add_cog(Moderation(client))
