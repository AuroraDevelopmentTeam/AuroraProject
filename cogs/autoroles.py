import asyncio
from typing import Optional
import emoji

import nextcord
from nextcord import Interaction, Message, Permissions, SlashOption
from nextcord.ext import commands, menus, application_checks
from nextcord.abc import GuildChannel

from core.auto.roles.getters import get_server_autorole_state, get_server_autorole_id, get_server_reaction_autorole, \
    check_level_autorole, list_level_autoroles, list_reaction_autoroles, check_reaction_autorole
from core.auto.roles.updaters import delete_autorole_for_reaction, write_autorole_for_reaction, \
    write_autorole_for_level, update_autorole_for_level, delete_autorole_for_level, set_autoroles_state, update_autorole
from core.embeds import DEFAULT_BOT_COLOR, construct_basic_embed
from core.locales.getters import get_msg_from_locale_by_key, get_localized_description, get_localized_name, \
    localize_name
from core.errors import construct_error_forbidden_embed, construct_error_negative_value_embed, \
    construct_error_http_exception_embed, construct_error_not_found_embed


class AutorolesList(menus.ListPageSource):
    def __init__(self, data, guild_id):
        self.guild_id = guild_id
        super().__init__(data, per_page=6)

    async def format_page(self, menu, entries) -> nextcord.Embed:
        embed = nextcord.Embed(title=localize_name(self.guild_id, "autorole").capitalize(), color=DEFAULT_BOT_COLOR)
        for entry in entries:
            embed.add_field(name=entry[0], value=entry[1], inline=False)
        embed.set_footer(text=f"{menu.current_page + 1}/{self.get_max_pages()}")
        return embed


class NoStopButtonMenuPages(menus.ButtonMenuPages, inherit_buttons=False):

    def __init__(self, source, timeout=60):
        super().__init__(source, timeout=timeout)

        # Add the buttons we want
        self.add_item(menus.MenuPaginationButton(emoji=self.FIRST_PAGE))
        self.add_item(menus.MenuPaginationButton(emoji=self.PREVIOUS_PAGE))
        self.add_item(menus.MenuPaginationButton(emoji=self.NEXT_PAGE))
        self.add_item(menus.MenuPaginationButton(emoji=self.LAST_PAGE))

        # Disable buttons that are unavailable to be pressed at the start
        self._disable_unavailable_buttons()


class Autorole(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_member_join(self, member):
        if get_server_autorole_state(member.guild.id) is False:
            return
        autorole_id = get_server_autorole_id(member.guild.id)
        if autorole_id == 0:
            return
        role = nextcord.utils.get(member.guild.roles, id=autorole_id)
        await member.add_roles(role)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):

        channel = await self.client.fetch_channel(payload.channel_id)
        member = payload.member
        if member.bot:
            return
        if get_server_autorole_state(member.guild.id) is False:
            return
        message = await channel.fetch_message(payload.message_id)
        emote = payload.emoji
        if emoji.emoji_count(str(emote)) >= 1:
            is_custom = False
        else:
            is_custom = True
        if is_custom is True:
            autoroles = get_server_reaction_autorole(channel.guild.id, channel.id, message.id, str(emote.id))
            if autoroles is None:
                return
            for autorole in autoroles:
                role = nextcord.utils.get(channel.guild.roles, id=autorole)
                await member.add_roles(role)
        else:
            emote = emoji.demojize(str(emote), delimiters=("", ""))
            autoroles = get_server_reaction_autorole(channel.guild.id, channel.id, message.id, str(emote))
            if autoroles is None:
                return
            for autorole in autoroles:
                role = nextcord.utils.get(channel.guild.roles, id=autorole)
                await member.add_roles(role)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        channel = await self.client.fetch_channel(payload.channel_id)
        member = payload.user_id
        member = nextcord.utils.get(channel.guild.members, id=member)
        if member.bot:
            return
        if get_server_autorole_state(member.guild.id) is False:
            return
        message = await channel.fetch_message(payload.message_id)
        emote = payload.emoji
        if emoji.emoji_count(str(emote)) >= 1:
            is_custom = False
        else:
            is_custom = True
        if is_custom is True:
            autoroles = get_server_reaction_autorole(channel.guild.id, channel.id, message.id, str(emote.id))
            if autoroles is None:
                return
            for autorole in autoroles:
                role = nextcord.utils.get(channel.guild.roles, id=autorole)
                await member.remove_roles(role)
        else:
            emote = emoji.demojize(str(emote), delimiters=("", ""))
            autoroles = get_server_reaction_autorole(channel.guild.id, channel.id, message.id, str(emote))
            if autoroles is None:
                return
            for autorole in autoroles:
                role = nextcord.utils.get(channel.guild.roles, id=autorole)
                await member.remove_roles(role)

    @nextcord.slash_command(
        name="autorole",
        description="Autoroles",
        name_localizations=get_localized_name("autorole"),
        description_localizations=get_localized_description("autorole"),
        default_member_permissions=Permissions(administrator=True),
    )
    @application_checks.has_permissions(manage_guild=True)
    async def __autorole(self, interaction: Interaction):
        pass

    @__autorole.subcommand(name="add_for_level", description="Add new autorole for indicated level",
                           name_localizations=get_localized_name("autorole_add_for_level"),
                           description_localizations=get_localized_description("autorole_add_for_level"),
                           )
    @application_checks.bot_has_guild_permissions(manage_roles=True)
    async def __autorole_for_level_add(self, interaction: Interaction,
                                       role: Optional[nextcord.Role] = SlashOption(required=True),
                                       level: Optional[int] = SlashOption(required=True)):
        try:
            if check_level_autorole(interaction.guild.id, level):
                update_autorole_for_level(interaction.guild.id, role, level)
            else:
                write_autorole_for_level(interaction.guild.id, role, level)
            message = get_msg_from_locale_by_key(
                interaction.guild.id, f"autorole_{interaction.application_command.name}"
            )
            message_2 = get_msg_from_locale_by_key(
                interaction.guild.id, f"autorole_{interaction.application_command.name}_2"
            )
            requested = get_msg_from_locale_by_key(interaction.guild.id, "requested_by")
            await interaction.response.send_message(
                embed=construct_basic_embed(
                    f"autorole_{interaction.application_command.name}",
                    f"{message} {level} {message_2} {role.mention}",
                    f"{requested} {interaction.user}",
                    interaction.user.display_avatar, interaction.guild.id
                )
            )
        except nextcord.Forbidden:
            return await interaction.response.send_message(
                embed=construct_error_forbidden_embed(
                    get_msg_from_locale_by_key(interaction.guild.id, "forbidden_error"),
                    self.client.user.avatar.url,
                )
            )

    @__autorole.subcommand(name="remove_for_level", description="Add new autorole for indicated level",
                           name_localizations=get_localized_name("autorole_remove_for_level"),
                           description_localizations=get_localized_description("autorole_remove_for_level"),
                           )
    async def __autorole_for_level_remove(self, interaction: Interaction,
                                          level: Optional[int] = SlashOption(required=True)):
        if level <= 1:
            return await interaction.response.send_message(
                embed=construct_error_negative_value_embed(
                    get_msg_from_locale_by_key(
                        interaction.guild.id, "negative_value_error"
                    ),
                    self.client.user.avatar.url,
                    level,
                )
            )
        if check_level_autorole(interaction.guild.id, level) is False:
            embed = nextcord.Embed(
                title="error",
                description=get_msg_from_locale_by_key(
                    interaction.guild.id, "no_in_table"
                ),
                color=DEFAULT_BOT_COLOR
            )
            return await interaction.response.send_message(embed=embed)
        delete_autorole_for_level(interaction.guild.id, level)
        message = get_msg_from_locale_by_key(
            interaction.guild.id, f"autorole_{interaction.application_command.name}"
        )
        requested = get_msg_from_locale_by_key(interaction.guild.id, "requested_by")
        await interaction.response.send_message(
            embed=construct_basic_embed(
                f"autorole_{interaction.application_command.name}",
                f"{message} **{level}**",
                f"{requested} {interaction.user}",
                interaction.user.display_avatar, interaction.guild.id
            )
        )

    @__autorole.subcommand(name="display_for_level",
                           description="Lists all autoroles for level",
                           name_localizations=get_localized_name("autorole_display_for_level"),
                           description_localizations=get_localized_description("autorole_display_for_level"),
                           )
    async def __autorole_for_level_display(self, interaction: Interaction):
        autoroles = list_level_autoroles(interaction.guild.id)
        source_for_pages = []
        for row in autoroles:
            role = nextcord.utils.get(interaction.guild.roles, id=row[0])
            role = role.mention
            lvl_msg = get_msg_from_locale_by_key(interaction.guild.id, "level").capitalize()
            level = f"{lvl_msg} {row[1]}"
            source_for_pages.append([level, role])
        pages = NoStopButtonMenuPages(
            source=AutorolesList(source_for_pages, interaction.guild.id),
        )
        await pages.start(interaction=interaction)

    @__autorole.subcommand(name="add_on_reaction",
                           description="Add new autorole on reaction",
                           name_localizations=get_localized_name("autorole_add_on_reaction"),
                           description_localizations=get_localized_description("autorole_add_on_reaction"),
                           )
    @application_checks.bot_has_guild_permissions(manage_roles=True)
    async def __autorole_on_reaction_add(self, interaction: Interaction,
                                         channel: Optional[GuildChannel] = SlashOption(required=True),
                                         message_id: Optional[str] = SlashOption(required=True),
                                         role: Optional[nextcord.Role] = SlashOption(required=True)):
        try:
            await interaction.response.defer()
            message_id = int(message_id)
            message = await channel.fetch_message(message_id)

            embed = nextcord.Embed(
                description=get_msg_from_locale_by_key(
                    interaction.guild.id, "react_here"
                ),
                color=DEFAULT_BOT_COLOR
            )

            message_for_reaction = await interaction.followup.send(embed=embed)

            def check(reaction, user):
                return (reaction.message.id == message_for_reaction.id) and (user.id == interaction.user.id)
            try:
                reaction, user = await self.client.wait_for('reaction_add', check=check, timeout=60)
            except asyncio.TimeoutError as error:
                embed = nextcord.Embed(
                    color=DEFAULT_BOT_COLOR, description=f"{error}"
                )
                return await interaction.followup.send(embed=embed)
            await message.add_reaction(str(reaction.emoji))
            if emoji.emoji_count(str(reaction.emoji)) >= 1:
                is_custom = False
            else:
                is_custom = True
            if is_custom is True:
                write_autorole_for_reaction(interaction.guild.id, channel.id, message.id, str(reaction.emoji.id), role,
                                            is_custom)
            else:
                emote = emoji.demojize(str(reaction.emoji), delimiters=("", ""))
                write_autorole_for_reaction(interaction.guild.id, channel.id, message.id, str(emote), role, is_custom)
            message = get_msg_from_locale_by_key(
                interaction.guild.id, f"autorole_{interaction.application_command.name}"
            )
            message_2 = get_msg_from_locale_by_key(
                interaction.guild.id, f"autorole_{interaction.application_command.name}_2"
            )
            requested = get_msg_from_locale_by_key(interaction.guild.id, "requested_by")
            await interaction.followup.send(
                embed=construct_basic_embed(
                    f"autorole_{interaction.application_command.name}",
                    f"{message} {reaction.emoji} {message_2} {role.mention}",
                    f"{requested} {interaction.user}",
                    interaction.user.display_avatar, interaction.guild.id
                )
            )
        except nextcord.NotFound:
            return await interaction.followup.send(
                embed=construct_error_not_found_embed(
                    get_msg_from_locale_by_key(
                        interaction.guild.id, "not_found_error"
                    ),
                    self.client.user.avatar.url,
                )
            )
        except AttributeError:
            return await interaction.followup.send(
                embed=construct_error_negative_value_embed(
                    get_msg_from_locale_by_key(
                        interaction.guild.id, "negative_value_error"
                    ),
                    self.client.user.avatar.url,
                    channel,
                )
            )
        except ValueError:
            return await interaction.followup.send(
                embed=construct_error_negative_value_embed(
                    get_msg_from_locale_by_key(
                        interaction.guild.id, "negative_value_error"
                    ),
                    self.client.user.avatar.url,
                    message_id,
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

    @__autorole.subcommand(name="remove_on_reaction",
                           description="Add new autorole on reaction",
                           name_localizations=get_localized_name("autorole_remove_on_reaction"),
                           description_localizations=get_localized_description("autorole_remove_on_reaction"),
                           )
    async def __autorole_on_reaction_remove(self, interaction: Interaction,
                                            role: Optional[nextcord.Role] = SlashOption(required=True)):
        if check_reaction_autorole(interaction.guild.id, role) is False:
            embed = nextcord.Embed(
                title="error",
                description=get_msg_from_locale_by_key(
                    interaction.guild.id, "no_in_table"
                ),
                color=DEFAULT_BOT_COLOR
            )
            return await interaction.response.send_message(embed=embed)
        delete_autorole_for_reaction(interaction.guild.id, role)
        message = get_msg_from_locale_by_key(
            interaction.guild.id, f"autorole_{interaction.application_command.name}"
        )
        requested = get_msg_from_locale_by_key(interaction.guild.id, "requested_by")
        await interaction.response.send_message(
            embed=construct_basic_embed(
                f"autorole_{interaction.application_command.name}",
                f"{message} {role.mention}",
                f"{requested} {interaction.user}",
                interaction.user.display_avatar, interaction.guild.id
            )
        )

    @__autorole.subcommand(name="display_on_reaction", description="Show all autoroles that must be given automatically",
                           name_localizations=get_localized_name("autorole_display_on_reaction"),
                           description_localizations=get_localized_description("autorole_display_on_reaction"),
                           )
    async def __autorole_on_reaction_display(self, interaction: Interaction):
        autoroles = list_reaction_autoroles(interaction.guild.id)
        source_for_pages = []
        for row in autoroles:
            role = nextcord.utils.get(interaction.guild.roles, id=row[0])
            role = role.mention
            reaction = f"e ID: {row[1]}"
            source_for_pages.append([reaction, role])
        pages = NoStopButtonMenuPages(
            source=AutorolesList(source_for_pages, interaction.guild.id),
        )
        await pages.start(interaction=interaction)

    @__autorole.subcommand(
        name="enable",
        description="Turn on or turn off autoroles for new guests of server",
        name_localizations=get_localized_name("autorole_enable"),
        description_localizations=get_localized_description("autorole_enable"),
    )
    async def __autoroles_state_set(
            self,
            interaction: Interaction,
            autoroles_state: int = SlashOption(
                name="picker", choices={"turn on": 1, "turn off": 0}, required=True
            ),
    ):
        autoroles_state = bool(autoroles_state)
        set_autoroles_state(interaction.guild.id, autoroles_state)
        message = get_msg_from_locale_by_key(
            interaction.guild.id, f"autorole_{interaction.application_command.name}"
        )
        requested = get_msg_from_locale_by_key(interaction.guild.id, "requested_by")
        if autoroles_state is True:
            autoroles_state = get_msg_from_locale_by_key(
                interaction.guild.id, "enabled"
            )
        else:
            autoroles_state = get_msg_from_locale_by_key(
                interaction.guild.id, "disabled"
            )
        await interaction.response.send_message(
            embed=construct_basic_embed(
                f"autorole_{interaction.application_command.name}",
                f"{message} **{autoroles_state}**",
                f"{requested} {interaction.user}",
                interaction.user.display_avatar, interaction.guild.id
            )
        )

    @__autorole.subcommand(
        name="on_enter",
        description="Turn on or turn off autoroles for new guests of server",
        name_localizations=get_localized_name("autorole_on_enter"),
        description_localizations=get_localized_description("autorole_on_enter"),
    )
    @application_checks.bot_has_guild_permissions(manage_roles=True)
    async def __autorole_set(
            self,
            interaction: Interaction,
            role: Optional[nextcord.Role] = SlashOption(required=True),
    ):
        try:
            update_autorole(interaction.guild.id, role.id)
            message = get_msg_from_locale_by_key(
                interaction.guild.id, f"autorole_{interaction.application_command.name}"
            )
            requested = get_msg_from_locale_by_key(interaction.guild.id, "requested_by")
            await interaction.response.send_message(
                embed=construct_basic_embed(
                    f"autorole_{interaction.application_command.name}",
                    f"{message} **{role.mention}**",
                    f"{requested} {interaction.user}",
                    interaction.user.display_avatar, interaction.guild.id
                )
            )
        except nextcord.Forbidden:
            return await interaction.response.send_message(
                embed=construct_error_forbidden_embed(
                    get_msg_from_locale_by_key(interaction.guild.id, "forbidden_error"),
                    self.client.user.avatar.url,
                )
            )


def setup(client):
    client.add_cog(Autorole(client))
