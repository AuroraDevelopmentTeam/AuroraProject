import datetime

import humanfriendly
from typing import Optional
import nextcord
from nextcord.ext import commands, application_checks
from nextcord import Interaction, SlashOption, Permissions

from core.errors import (
    construct_error_forbidden_embed,
    construct_error_limit_break_embed,
    construct_error_http_exception_embed,
    construct_error_negative_value_embed,
    construct_error_bot_user_embed,
)
from core.embeds import construct_basic_embed, construct_top_embed
from core.locales.getters import (
    get_msg_from_locale_by_key,
    get_localized_description,
    get_localized_name,
    localize_name,
)
from core.parsers import parse_timeouts, parse_warns_of_user
from core.warns.writers import write_new_warn
from core.warns.updaters import remove_warn_from_table, update_warn_reason
from core.warns.getters import check_warn, get_warn_reason
from core.checkers import is_warn_id_in_table
from core.embeds import DEFAULT_BOT_COLOR


class Moderation(commands.Cog):
    def __init__(self, client):
        self.client = client

    @nextcord.slash_command(
        name="mute",
        description="Mute with timeout discord's user",
        name_localizations=get_localized_name("mute"),
        description_localizations=get_localized_description("mute"),
        default_member_permissions=Permissions(moderate_members=True),
    )
    @application_checks.has_permissions(moderate_members=True)
    async def __mute(
        self,
        interaction: Interaction,
        user: Optional[nextcord.Member] = SlashOption(
            required=True,
            description="The discord's user, tag someone with @",
            name_localizations={"ru": "пользователь"},
            description_localizations={
                "ru": "Пользователь дискорда, укажите кого-то @"
            },
        ),
        time: Optional[str] = SlashOption(
            required=True,
            description="Time of mute, 1h/2h/3d",
            name_localizations={"ru": "время"},
            description_localizations={
                "ru": "Время мута, напишите в формате: 1h/2h/3d"
            },
        ),
        *,
        reason: Optional[str] = SlashOption(
            required=False,
            description="Reason of giving mute",
            name_localizations={"ru": "причина"},
            description_localizations={
                "ru": "Причина выдаваемого мута"
            },
        )
    ):
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
        if user.bot:
            return await interaction.response.send_message(
                embed=construct_error_bot_user_embed(
                    get_msg_from_locale_by_key(interaction.guild.id, "bot_user_error"),
                    self.client.user.avatar.url,
                )
            )
        try:
            time_in_seconds = humanfriendly.parse_timespan(time)
            if time_in_seconds <= 0:
                return await interaction.response.send_message(
                    embed=construct_error_negative_value_embed(
                        get_msg_from_locale_by_key(
                            interaction.guild.id, "negative_value_error"
                        ),
                        self.client.user.avatar.url,
                        time_in_seconds,
                    )
                )
            requested = get_msg_from_locale_by_key(interaction.guild.id, "requested_by")
            if reason is None:
                reason = " — "
            await user.edit(
                timeout=nextcord.utils.utcnow()
                + datetime.timedelta(seconds=time_in_seconds),
                reason=reason,
            )
            message = get_msg_from_locale_by_key(
                interaction.guild.id, interaction.application_command.name
            )
            await interaction.response.send_message(
                embed=construct_basic_embed(
                    interaction.application_command.name,
                    f"{message} {user.mention}",
                    f"📝 {reason}. 🕔 {time}\n{requested} {interaction.user}",
                    interaction.user.display_avatar, interaction.guild.id
                )
            )
        except nextcord.Forbidden:
            await interaction.response.send_message(
                embed=construct_error_forbidden_embed(
                    get_msg_from_locale_by_key(interaction.guild.id, "forbidden_error"),
                    self.client.user.avatar.url,
                )
            )
        except humanfriendly.InvalidTimespan:
            embed = nextcord.Embed(
                title="mute_invalid_timespan",
                description=get_msg_from_locale_by_key(
                    interaction.guild.id, "mute_invalid_timespan"
                ),
                color=DEFAULT_BOT_COLOR
            )
            return await interaction.response.send_message(embed=embed)

    @nextcord.slash_command(
        name="unmute",
        description="Unmute muted (timed out) discord user",
        name_localizations=get_localized_name("unmute"),
        description_localizations=get_localized_description("unmute"),
        default_member_permissions=Permissions(moderate_members=True),
    )
    @application_checks.has_permissions(moderate_members=True)
    async def __unmute(
        self,
        interaction: Interaction,
        user: Optional[nextcord.Member] = SlashOption(
            required=True,
            description="The discord's user, tag someone with @",
            name_localizations={"ru": "пользователь"},
            description_localizations={
                "ru": "Пользователь дискорда, укажите кого-то @"
            },
        ),
    ):
        """
        Parameters
        ----------
        interaction: Interaction
            The interaction object
        user: Optional[nextcord.Member]
            The discord's user, tag someone with @
        """
        if user.bot:
            return await interaction.response.send_message(
                embed=construct_error_bot_user_embed(
                    get_msg_from_locale_by_key(interaction.guild.id, "bot_user_error"),
                    self.client.user.avatar.url,
                )
            )
        if user.timeout is None:
            embed = nextcord.Embed(
                title="No mute",
                description=get_msg_from_locale_by_key(
                    interaction.guild.id, "no_mute"
                ),
                color=DEFAULT_BOT_COLOR
            )
            return await interaction.response.send_message(embed=embed)
        try:
            requested = get_msg_from_locale_by_key(interaction.guild.id, "requested_by")
            await user.edit(timeout=None)
            message = get_msg_from_locale_by_key(
                interaction.guild.id, interaction.application_command.name
            )
            await interaction.response.send_message(
                embed=construct_basic_embed(
                    interaction.application_command.name,
                    f"{message} {user.mention}",
                    f"{requested} {interaction.user}",
                    interaction.user.display_avatar, interaction.guild.id
                )
            )
        except nextcord.Forbidden:
            await interaction.response.send_message(
                embed=construct_error_forbidden_embed(
                    get_msg_from_locale_by_key(interaction.guild.id, "forbidden_error"),
                    self.client.user.avatar.url,
                )
            )


    @nextcord.slash_command(
        name="mutes",
        description="Show list of active mutes on this server",
        name_localizations=get_localized_name("mutes"),
        description_localizations=get_localized_description("mutes"),
        default_member_permissions=Permissions(send_messages=True),
    )
    async def __mutes(self, interaction: Interaction):
        """
        Parameters
        ----------
        interaction: Interaction
            The interaction object
        """
        await interaction.response.defer()
        requested = get_msg_from_locale_by_key(interaction.guild.id, "requested_by")
        mutes = parse_timeouts(interaction.guild.members)
        await interaction.followup.send(
            embed=construct_top_embed(
                interaction.application_command.name,
                mutes,
                f"{requested} {interaction.user}",
                interaction.user.display_avatar,
            )
        )

    @nextcord.slash_command(
        name="clear",
        description="Deletes messages in channel, where command was used",
        name_localizations=get_localized_name("clear"),
        description_localizations=get_localized_description("clear"),
        default_member_permissions=Permissions(administrator=True),
    )
    @application_checks.has_permissions(manage_guild=True)
    async def __clear(
        self,
        interaction: Interaction,
        messages_to_delete: Optional[int] = SlashOption(required=True),
        *,
        before=None,
        after=None,
    ):
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
        await interaction.response.defer()
        if messages_to_delete <= 0:
            return await interaction.followup.send(
                embed=construct_error_negative_value_embed(
                    get_msg_from_locale_by_key(
                        interaction.guild.id, "negative_value_error"
                    ),
                    self.client.user.avatar.url,
                    messages_to_delete,
                )
            )
        if messages_to_delete > 1000:
            return await interaction.followup.send(
                embed=construct_error_limit_break_embed(
                    get_msg_from_locale_by_key(interaction.guild.id, "limit_break"),
                    self.client.user.avatar.url,
                )
            )
        message = await interaction.followup.send(f"/{localize_name(interaction.guild.id, 'clear')}...")
        if before is None:
            before = message.created_at
        else:
            before = nextcord.Object(id=before)

        if after is not None:
            after = nextcord.Object(id=after)

        try:
            were_deleted = await interaction.channel.purge(
                limit=messages_to_delete, before=before, after=after
            )
            requested = get_msg_from_locale_by_key(interaction.guild.id, "requested_by")
            message = get_msg_from_locale_by_key(
                interaction.guild.id, interaction.application_command.name
            )
            await interaction.followup.send(
                embed=construct_basic_embed(
                    interaction.application_command.name,
                    f"{message} **{len(were_deleted)}**",
                    f"{requested} {interaction.user}",
                    interaction.user.display_avatar, interaction.guild.id
                )
            )
        except nextcord.Forbidden:
            return await interaction.followup.send(
                embed=construct_error_forbidden_embed(
                    get_msg_from_locale_by_key(interaction.guild.id, "forbidden_error"),
                    self.client.user.avatar.url,
                )
            )
        except nextcord.HTTPException:
            return await interaction.followup.send(
                embed=construct_error_http_exception_embed(
                    get_msg_from_locale_by_key(interaction.guild.id, "http_exception"),
                    self.client.user.avatar.url,
                )
            )

    @nextcord.slash_command(
        name="warn",
        description="Warn's user on your server",
        name_localizations=get_localized_name("warn"),
        description_localizations=get_localized_description("warn"),
        default_member_permissions=Permissions(manage_messages=True),
    )
    @application_checks.has_permissions(manage_messages=True)
    async def __warn(
        self,
        interaction: Interaction,
        user: Optional[nextcord.Member] = SlashOption(required=True),
        reason: Optional[str] = SlashOption(required=False),
    ):
        await interaction.response.defer()
        try:
            if user.bot:
                return await interaction.response.send_message("bot_user_error")
            if reason is None:
                reason = " — "
            write_new_warn(interaction.guild.id, user.id, reason)
            requested = get_msg_from_locale_by_key(interaction.guild.id, "requested_by")
            message = get_msg_from_locale_by_key(
                interaction.guild.id, interaction.application_command.name
            )
            warns = parse_warns_of_user(interaction.guild.id, user.id)
            await interaction.followup.send(
                embed=construct_basic_embed(
                    interaction.application_command.name,
                    f"{message} {user.mention}",
                    f"📝 {reason}.\n{requested} {interaction.user}",
                    interaction.user.display_avatar, interaction.guild.id
                )
            )
            if (len(warns)) == 3:
                for warn in warns:
                    warn_id = warn[0]
                    remove_warn_from_table(warn_id, interaction.guild.id, user.id)
                await user.edit(
                    timeout=nextcord.utils.utcnow() + datetime.timedelta(seconds=3600),
                    reason=reason,
                )
                message = get_msg_from_locale_by_key(interaction.guild.id, "mute")
                await interaction.followup.send(
                    embed=construct_basic_embed(
                        "Автомут за 3 варна и их очищение",
                        f"{message} {user.mention}",
                        f"📝 {reason}. 🕔 1 h\n{requested} {interaction.user}",
                        interaction.user.display_avatar, interaction.guild.id
                    )
                )
        except nextcord.Forbidden:
            await interaction.followup.send(
                embed=construct_error_forbidden_embed(
                    "**Автомут за 3  варна и их очищение**\n"
                    + get_msg_from_locale_by_key(
                        interaction.guild.id, "forbidden_error"
                    ),
                    self.client.user.avatar.url,
                )
            )

    @nextcord.slash_command(
        name="unwarn",
        description="Remove warn from user on your server",
        name_localizations=get_localized_name("unwarn"),
        description_localizations=get_localized_description("unwarn"),
        default_member_permissions=Permissions(manage_messages=True),
    )
    @application_checks.has_permissions(manage_messages=True)
    async def __unwarn(
        self,
        interaction: Interaction,
        user: Optional[nextcord.Member] = SlashOption(required=True),
        warn_id: Optional[int] = SlashOption(required=True),
    ):
        if user.bot:
            return await interaction.response.send_message(
                embed=construct_error_bot_user_embed(
                    get_msg_from_locale_by_key(interaction.guild.id, "bot_user_error"),
                    self.client.user.avatar.url,
                )
            )
        warns = parse_warns_of_user(interaction.guild.id, user.id)
        if len(warns) == 0:
            embed = nextcord.Embed(
                title="error",
                description=get_msg_from_locale_by_key(
                    interaction.guild.id, "user_no_warns"
                ),
                color=DEFAULT_BOT_COLOR
            )
            return await interaction.response.send_message(embed=embed)
        if is_warn_id_in_table("warns", warn_id, interaction.guild.id, user.id) is True:
            remove_warn_from_table(warn_id, interaction.guild.id, user.id)
            requested = get_msg_from_locale_by_key(interaction.guild.id, "requested_by")
            message = get_msg_from_locale_by_key(
                interaction.guild.id, interaction.application_command.name
            )
            await interaction.response.send_message(
                embed=construct_basic_embed(
                    interaction.application_command.name,
                    f"{message} {user.mention}",
                    f"ID#{warn_id}\n{requested} {interaction.user}",
                    interaction.user.display_avatar, interaction.guild.id
                )
            )
        else:
            embed = nextcord.Embed(
                title="error",
                description=get_msg_from_locale_by_key(
                    interaction.guild.id, "no_warn_in_table"
                ),
                color=DEFAULT_BOT_COLOR
            )
            return await interaction.response.send_message(embed=embed)

    @nextcord.slash_command(
        name="warns",
        description="View warns of @User on your server",
        name_localizations=get_localized_name("warns"),
        description_localizations=get_localized_description("warns"),
        default_member_permissions=Permissions(send_messages=True),
    )
    async def __warns(
        self,
        interaction: Interaction,
        user: Optional[nextcord.Member] = SlashOption(required=True),
    ):
        await interaction.response.defer()
        if user.bot:
            return await interaction.followup.send(
                embed=construct_error_bot_user_embed(
                    get_msg_from_locale_by_key(interaction.guild.id, "bot_user_error"),
                    self.client.user.avatar.url,
                )
            )
        requested = get_msg_from_locale_by_key(interaction.guild.id, "requested_by")
        warns = parse_warns_of_user(interaction.guild.id, user.id)
        await interaction.followup.send(
            embed=construct_top_embed(
                f"{interaction.application_command.name} - {user}",
                warns,
                f"{requested} {interaction.user}",
                interaction.user.display_avatar,
            )
        )

    @nextcord.slash_command(
        name="edit_warn",
        description="Edit warn with this id on your server",
        name_localizations=get_localized_name("edit_warn"),
        description_localizations=get_localized_description("edit_warn"),
        default_member_permissions=Permissions(manage_messages=True),
    )
    @application_checks.has_permissions(manage_messages=True)
    async def __edit_warn(
        self,
        interaction: Interaction,
        warn_id: Optional[int] = SlashOption(required=True),
        new_warn_reason: Optional[str] = SlashOption(required=True),
    ):
        if check_warn(interaction.guild.id, warn_id) is False:
            embed = nextcord.Embed(
                title="error",
                description=get_msg_from_locale_by_key(
                    interaction.guild.id, "no_warn_in_table"
                ),
                color=DEFAULT_BOT_COLOR
            )
            return await interaction.response.send_message(embed=embed)
        update_warn_reason(interaction.guild.id, warn_id, new_warn_reason)
        message = get_msg_from_locale_by_key(
            interaction.guild.id, f"{interaction.application_command.name}"
        )
        requested = get_msg_from_locale_by_key(interaction.guild.id, "requested_by")
        await interaction.response.send_message(
            embed=construct_basic_embed(
                interaction.application_command.name,
                f"{message} {new_warn_reason}",
                f"{requested} {interaction.user}",
                interaction.user.display_avatar, interaction.guild.id
            )
        )

    @nextcord.slash_command(
        name="purge_warns",
        description="remove all warns from user",
        name_localizations=get_localized_name("purge_warns"),
        description_localizations=get_localized_description("purge_warns"),
        default_member_permissions=Permissions(manage_messages=True),
    )
    @application_checks.has_permissions(manage_messages=True)
    async def __purge_warns(
        self, interaction: Interaction, user: Optional[nextcord.Member]
    ):
        if user.bot:
            return await interaction.response.send_message(
                embed=construct_error_bot_user_embed(
                    get_msg_from_locale_by_key(interaction.guild.id, "bot_user_error"),
                    self.client.user.avatar.url,
                )
            )
        warns = parse_warns_of_user(interaction.guild.id, user.id)
        if len(warns) == 0:
            embed = nextcord.Embed(
                title="error",
                description=get_msg_from_locale_by_key(
                    interaction.guild.id, "user_no_warns"
                ),
                color=DEFAULT_BOT_COLOR
            )
            return await interaction.response.send_message(embed=embed)
        for warn in warns:
            warn_id = warn[0]
            remove_warn_from_table(warn_id, interaction.guild.id, user.id)
        requested = get_msg_from_locale_by_key(interaction.guild.id, "requested_by")
        message = get_msg_from_locale_by_key(
            interaction.guild.id, interaction.application_command.name
        )
        await interaction.response.send_message(
            embed=construct_basic_embed(
                interaction.application_command.name,
                f"{message} {user.mention}",
                f"{requested} {interaction.user}",
                interaction.user.display_avatar, interaction.guild.id
            )
        )


def setup(client):
    client.add_cog(Moderation(client))
