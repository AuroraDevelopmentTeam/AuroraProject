import datetime

import humanfriendly
from typing import Optional
import nextcord
from nextcord.ext import commands
from nextcord import Interaction, SlashOption, Permissions

from core.errors import construct_error_forbidden_embed, construct_error_limit_break_embed, \
    construct_error_http_exception_embed
from core.embeds import construct_basic_embed, construct_top_embed
from core.locales.getters import get_msg_from_locale_by_key
from core.parsers import parse_timeouts, parse_warns_of_user
from core.warns.writers import write_new_warn
from core.warns.updaters import remove_warn_from_table
from core.checkers import is_warn_id_in_table


class Moderation(commands.Cog):
    def __init__(self, client):
        self.client = client

    @nextcord.slash_command(name="mute", description="Mute with timeout discord's user",
                            default_member_permissions=Permissions(moderate_members=True))
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
            if reason is None:
                reason = ' — '
            await user.edit(timeout=nextcord.utils.utcnow() + datetime.timedelta(seconds=time_in_seconds),
                            reason=reason)
            message = get_msg_from_locale_by_key(interaction.guild.id, interaction.application_command.name)
            await interaction.response.send_message(
                embed=construct_basic_embed(interaction.application_command.name,
                                            f"{message} {user.mention}",
                                            f"📝 {reason}. 🕔 {time}\n{requested} {interaction.user}",
                                            interaction.user.display_avatar))
        except nextcord.Forbidden:
            await interaction.response.send_message(
                embed=construct_error_forbidden_embed(
                    get_msg_from_locale_by_key(interaction.guild.id, 'forbidden_error'),
                    self.client.user.avatar.url)
            )

    @nextcord.slash_command(name="unmute", description="Unmute muted (timed out) discord user",
                            default_member_permissions=Permissions(moderate_members=True))
    async def __unmute(self, interaction: Interaction, user: Optional[nextcord.Member] = SlashOption(required=True)):
        """
        Parameters
        ----------
        interaction: Interaction
            The interaction object
        user: Optional[nextcord.Member]
            The discord's user, tag someone with @
        """
        try:
            requested = get_msg_from_locale_by_key(interaction.guild.id, 'requested_by')
            await user.edit(timeout=None)
            message = get_msg_from_locale_by_key(interaction.guild.id, interaction.application_command.name)
            await interaction.response.send_message(
                embed=construct_basic_embed(interaction.application_command.name,
                                            f"{message} {user.mention}",
                                            f"{requested} {interaction.user}",
                                            interaction.user.display_avatar))
        except nextcord.Forbidden:
            await interaction.response.send_message(
                embed=construct_error_forbidden_embed(
                    get_msg_from_locale_by_key(interaction.guild.id, 'forbidden_error'),
                    self.client.user.avatar.url)
            )

    @nextcord.slash_command(name="mutes", description="Show list of active mutes on this server",
                            default_member_permissions=Permissions(send_messages=True))
    async def __mutes(self, interaction: Interaction):
        """
        Parameters
        ----------
        interaction: Interaction
            The interaction object
        """
        requested = get_msg_from_locale_by_key(interaction.guild.id, 'requested_by')
        mutes = parse_timeouts(interaction.guild.members)
        await interaction.response.send_message(
            embed=construct_top_embed(interaction.application_command.name, mutes,
                                      f"{requested} {interaction.user}", interaction.user.display_avatar))

    @nextcord.slash_command(name="clear", description="Deletes messages in channel, where command was used",
                            default_member_permissions=Permissions(administrator=True))
    async def __clear(self, interaction: Interaction,
                      messages_to_delete: Optional[int] = SlashOption(required=True),
                      *, before=None, after=None):
        """
        Parameters
        ----------
        interaction: Interaction
            The interaction object
        messages_to_delete: Optional[int]
            How many messages i should delete, command limited to 1000 messages in one execution
        before
            ID of message, BEFORE THIS message deletion will take place
        after
            ID of message, AFTER THIS message deletion will take place
        """
        if messages_to_delete > 1000:
            return await interaction.response.send_message(
                embed=construct_error_limit_break_embed(
                    get_msg_from_locale_by_key(interaction.guild.id, 'limit_break'),
                    self.client.user.avatar.url)
            )
        if before is None:
            before = interaction.message
        else:
            before = nextcord.Object(id=before)

        if after is not None:
            after = nextcord.Object(id=after)

        try:
            were_deleted = await interaction.channel.purge(limit=messages_to_delete, before=before, after=after)
            requested = get_msg_from_locale_by_key(interaction.guild.id, 'requested_by')
            message = get_msg_from_locale_by_key(interaction.guild.id, interaction.application_command.name)
            await interaction.response.send_message(
                embed=construct_basic_embed(interaction.application_command.name,
                                            f"{message} {len(were_deleted)}",
                                            f"{requested} {interaction.user}",
                                            interaction.user.display_avatar))
        except nextcord.Forbidden:
            return await interaction.response.send_message(
                embed=construct_error_forbidden_embed(
                    get_msg_from_locale_by_key(interaction.guild.id, 'forbidden_error'),
                    self.client.user.avatar.url)
            )
        except nextcord.HTTPException:
            return await interaction.response.send_message(
                embed=construct_error_http_exception_embed(
                    get_msg_from_locale_by_key(interaction.guild.id, 'http_exception'),
                    self.client.user.avatar.url)
            )

    @nextcord.slash_command(name="warn", description="Warn's user on your server",
                            default_member_permissions=Permissions(manage_messages=True))
    async def __warn(self, interaction: Interaction, user: Optional[nextcord.Member] = SlashOption(required=True),
                     reason: Optional[str] = SlashOption(required=False)):
        if reason is None:
            reason = ' — '
        write_new_warn(interaction.guild.id, user.id, reason)
        requested = get_msg_from_locale_by_key(interaction.guild.id, 'requested_by')
        message = get_msg_from_locale_by_key(interaction.guild.id, interaction.application_command.name)
        await interaction.response.send_message(
            embed=construct_basic_embed(interaction.application_command.name,
                                        f"{message} {user.mention}",
                                        f"📝 {reason}.\n{requested} {interaction.user}",
                                        interaction.user.display_avatar))

    @nextcord.slash_command(name="unwarn", description="Remove warn from user on your server",
                            default_member_permissions=Permissions(manage_messages=True))
    async def __unwarn(self, interaction: Interaction, user: Optional[nextcord.Member] = SlashOption(required=True),
                       warn_id: Optional[int] = SlashOption(required=True)):
        if is_warn_id_in_table("warns", warn_id, interaction.guild.id, user.id) is True:
            remove_warn_from_table(warn_id, interaction.guild.id, user.id)
            requested = get_msg_from_locale_by_key(interaction.guild.id, 'requested_by')
            message = get_msg_from_locale_by_key(interaction.guild.id, interaction.application_command.name)
            await interaction.response.send_message(
                embed=construct_basic_embed(interaction.application_command.name,
                                            f"{message} {user.mention}",
                                            f"ID#{warn_id}\n{requested} {interaction.user}",
                                            interaction.user.display_avatar))
        else:
            await interaction.response.send_message('no value in db error')

    @nextcord.slash_command(name="warns", description="View warns of @User on your server",
                            default_member_permissions=Permissions(send_messages=True))
    async def __warns(self, interaction: Interaction, user: Optional[nextcord.Member] = SlashOption(required=True)):
        """
        Parameters
        ----------
        interaction: Interaction
            The interaction object
        """
        requested = get_msg_from_locale_by_key(interaction.guild.id, 'requested_by')
        warns = parse_warns_of_user(interaction.guild.id, user.id)
        await interaction.response.send_message(
            embed=construct_top_embed(f"{interaction.application_command.name} - {user}", warns,
                                      f"{requested} {interaction.user}", interaction.user.display_avatar))


def setup(client):
    client.add_cog(Moderation(client))
