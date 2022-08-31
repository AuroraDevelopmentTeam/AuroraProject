from typing import Optional

import nextcord
from nextcord.ext import commands, application_checks
from nextcord.abc import GuildChannel
from nextcord import (
    Interaction,
    Permissions,
    SlashOption,
    AutoModerationTriggerType,
    AutoModerationAction,
    AutoModerationActionType,
    AutoModerationEventType,
    AutoModerationActionMetadata,
    AutoModerationTriggerMetadata,
)

from core.embeds import DEFAULT_BOT_COLOR, construct_basic_embed
from core.auto.mod.getters import (
    get_server_moderation_mode,
    get_server_link_detect,
    get_server_word_detect,
    get_server_status_detect,
    get_server_nickname_detect,
    fetchall_mod_words,
)
from core.auto.mod.updaters import (
    update_server_link_detect,
    update_server_nickname_detect,
    update_server_status_detect,
    update_server_word_detect,
    update_server_moderation_mode,
)
from core.auto.mod.writers import write_in_mod_word, delete_mod_word
from core.locales.getters import (
    get_msg_from_locale_by_key,
    get_localized_description,
    get_localized_name,
    get_guild_locale,
)
from core.errors import construct_error_not_found_embed

block_links = [
    "discord.gg*",
    "https:*",
    "http:*",
    "https://discord.gg/*",
    "discord.gg",
    "https:",
    "http:",
]
allow_list = [
    "imgur",
    "https://github.com/",
    "github.io",
    "github",
    "google",
    "yandex",
    "tenor",
    "pinterest",
    "https://discord.com/",
    "vk",
    "vk.com",
    "facebook",
    "https://vk.com/",
    "youtube",
    "https://www.youtube.com/",
]


class AutoModeration(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_member_join(self, member: nextcord.Member):
        word_detect = get_server_word_detect(member.guild.id)
        if word_detect is False:
            return
        mod_words = None
        moderation_mode = get_server_moderation_mode(member.guild.id)
        if moderation_mode == "friends_group":
            mod_words = fetchall_mod_words(member.guild.id)
        elif moderation_mode == "community":
            try:
                auto_mod_rules = await member.guild.auto_moderation_rules()
                try:
                    aurora_automoderation_rule = nextcord.utils.get(
                        auto_mod_rules, name="Aurora-Automoderation"
                    )
                    mod_words = (
                        aurora_automoderation_rule.trigger_metadata.keyword_filter
                    )
                except AttributeError:
                    pass
            except nextcord.Forbidden:
                pass
            except nextcord.NotFound:
                pass

        nickname_detect = get_server_nickname_detect(member.guild.id)
        if mod_words is None:
            return
        if nickname_detect is True:
            member_nickname = member.name
            for word in mod_words:
                if word in member_nickname:
                    try:
                        await member.send(
                            get_msg_from_locale_by_key(
                                member.guild.id, "forbidden_nickname"
                            )
                        )
                        await member.guild.kick(member)
                        return
                    except nextcord.Forbidden:
                        pass
        status_detect = get_server_status_detect(member.guild.id)
        if status_detect is True:
            try:
                activity = member.activity.name
            except AttributeError:
                activity = member.activity
            member_activity = activity
            if member_activity is None:
                return
            for word in mod_words:
                if word in member_activity:
                    try:
                        await member.send(
                            get_msg_from_locale_by_key(
                                member.guild.id, "forbidden_description"
                            )
                        )
                        await member.guild.kick(member)
                    except nextcord.Forbidden:
                        pass

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        if (
            message.author.guild_permissions.ban_members is True
            or message.author.guild_permissions.kick_members is True
            or message.author.guild_permissions.moderate_members is True
            or message.author.guild_permissions.manage_channels is True
            or message.author.guild_permissions.administrator is True
            or message.author.guild_permissions.manage_guild is True
        ):
            return
        word_detect = get_server_word_detect(message.guild.id)
        if word_detect is False:
            return
        mod_words = None
        moderation_mode = get_server_moderation_mode(message.guild.id)
        if moderation_mode == "friends_group":
            mod_words = fetchall_mod_words(message.guild.id)
        elif moderation_mode == "community":
            try:
                auto_mod_rules = await message.guild.auto_moderation_rules()
                try:
                    aurora_automoderation_rule = nextcord.utils.get(
                        auto_mod_rules, name="Aurora-Automoderation"
                    )
                    mod_words = (
                        aurora_automoderation_rule.trigger_metadata.keyword_filter
                    )
                except AttributeError:
                    pass
            except nextcord.Forbidden:
                pass
            except nextcord.NotFound:
                pass
        if mod_words is None or len(mod_words) == 0:
            return
        nickname_detect = get_server_nickname_detect(message.guild.id)
        if nickname_detect is True:
            member_nickname = message.author.name
            for word in mod_words:
                if word in member_nickname:
                    try:
                        await message.author.send(
                            get_msg_from_locale_by_key(
                                member.guild.id, "forbidden_nickname"
                            )
                        )
                        await message.guild.kick(message.author)
                        return
                    except nextcord.Forbidden:
                        pass
        status_detect = get_server_status_detect(message.guild.id)
        if status_detect is True:
            try:
                activity = message.author.activity.name
            except AttributeError:
                activity = message.author.activity
            member_activity = activity
            if member_activity is None:
                return
            for word in mod_words:
                if word in member_activity:
                    try:
                        await message.author.send(
                            get_msg_from_locale_by_key(
                                member.guild.id, "forbidden_description"
                            )
                        )
                        await message.guild.kick(message.author)
                        return
                    except nextcord.Forbidden:
                        pass

        moderation_mode = get_server_moderation_mode(message.guild.id)
        if moderation_mode == "friends_group":
            word_detect = get_server_word_detect(message.guild.id)
            if word_detect is False:
                return
            else:
                mod_words = fetchall_mod_words(message.guild.id)
                message_content = message.content
                for word in mod_words:
                    if word in message_content:
                        await message.delete()
                        break
            if get_server_link_detect(message.guild.id) is True:
                for link in block_links:
                    if link in message_content:
                        await message.delete()
                        break
            else:
                return

    @application_checks.bot_has_guild_permissions(manage_guild=True)
    @application_checks.has_permissions(manage_guild=True)
    @nextcord.slash_command(
        name="automod",
        description="Automod system",
        name_localizations=get_localized_name("automod"),
        description_localizations=get_localized_description("automod"),
        default_member_permissions=Permissions(administrator=True),
    )
    @application_checks.has_permissions(manage_guild=True)
    async def __automod(self, interaction: Interaction):
        pass

    @application_checks.bot_has_guild_permissions(manage_guild=True)
    @application_checks.has_permissions(manage_guild=True)
    @__automod.subcommand(
        name="setup",
        description="Automod system setup",
        name_localizations=get_localized_name("automod_setup"),
        description_localizations=get_localized_description("automod_setup"),
    )
    async def __test_automod(self, interaction: Interaction):
        moderation_mode = get_server_moderation_mode(interaction.guild.id)
        if moderation_mode == "friends_group":
            embed = nextcord.Embed(
                color=DEFAULT_BOT_COLOR,
                description=f"{get_msg_from_locale_by_key(interaction.guild.id, 'only_community')}",
            )
            await interaction.response.send_message(embed=embed)
        else:
            try:
                auto_mod_rules = await interaction.guild.auto_moderation_rules()
                aurora_automoderation_rule = nextcord.utils.get(
                    auto_mod_rules, name="Aurora-Automoderation"
                )
                if aurora_automoderation_rule is None:
                    await interaction.guild.create_auto_moderation_rule(
                        name="Aurora-Automoderation",
                        trigger_type=AutoModerationTriggerType.keyword,
                        trigger_metadata=AutoModerationTriggerMetadata(
                            keyword_filter=[
                                "*пизд*",
                                "*шлюх*",
                                "*тварь*",
                                "*уебищ*",
                                "*хуй*",
                                "*ебал*",
                                "*fuck*",
                                "*cunt*",
                                "*idiot*",
                                "пизд",
                                "шлюх",
                                "тварь",
                                "уебищ",
                                "хуй",
                                "ебал",
                                "fuck",
                                "cunt",
                                "idiot",
                                "пизд",
                            ]
                        ),
                        event_type=AutoModerationEventType.message_send,
                        actions=[
                            AutoModerationAction(
                                metadata=AutoModerationActionMetadata(
                                    channel=None, duration_seconds=None
                                ),
                                type=AutoModerationActionType.block_message,
                            )
                        ],
                        enabled=True,
                    )
                    message = get_msg_from_locale_by_key(
                        interaction.guild.id,
                        f"automod_{interaction.application_command.name}",
                    )
                    requested = get_msg_from_locale_by_key(
                        interaction.guild.id, "requested_by"
                    )
                    await interaction.response.send_message(
                        embed=construct_basic_embed(
                            f"automod_{interaction.application_command.name}",
                            f"{message}",
                            f"{requested} {interaction.user}",
                            interaction.user.display_avatar,
                            interaction.guild.id,
                        )
                    )
                else:
                    message = get_msg_from_locale_by_key(
                        interaction.guild.id, f"already_automod"
                    )
                    requested = get_msg_from_locale_by_key(
                        interaction.guild.id, "requested_by"
                    )
                    await interaction.response.send_message(
                        embed=construct_basic_embed(
                            f"automod_{interaction.application_command.name}",
                            f"{message}",
                            f"{requested} {interaction.user}",
                            interaction.user.display_avatar,
                            interaction.guild.id,
                        )
                    )
            except nextcord.Forbidden:
                embed = nextcord.Embed(
                    color=DEFAULT_BOT_COLOR,
                    description=f"{get_msg_from_locale_by_key(interaction.guild.id, 'only_community')}",
                )
                return await interaction.response.send_message(embed=embed)
            except nextcord.NotFound:
                await interaction.guild.create_auto_moderation_rule(
                    name="Aurora-Automoderation",
                    trigger_type=AutoModerationTriggerType.keyword,
                    trigger_metadata=AutoModerationTriggerMetadata(
                        keyword_filter=[
                            "*пизд*",
                            "*шлюх*",
                            "*тварь*",
                            "*уебищ*",
                            "*хуй*",
                            "*ебал*",
                            "*fuck*",
                            "*cunt*",
                            "*idiot*",
                            "пизд",
                            "шлюх",
                            "тварь",
                            "уебищ",
                            "хуй",
                            "ебал",
                            "fuck",
                            "cunt",
                            "idiot",
                            "пизд",
                        ]
                    ),
                    event_type=AutoModerationEventType.message_send,
                    actions=[
                        AutoModerationAction(
                            metadata=AutoModerationActionMetadata(
                                channel=None, duration_seconds=None
                            ),
                            type=AutoModerationActionType.block_message,
                        )
                    ],
                    enabled=True,
                )
                message = get_msg_from_locale_by_key(
                    interaction.guild.id,
                    f"automod_{interaction.application_command.name}",
                )
                requested = get_msg_from_locale_by_key(
                    interaction.guild.id, "requested_by"
                )
                await interaction.response.send_message(
                    embed=construct_basic_embed(
                        f"automod_{interaction.application_command.name}",
                        f"{message}",
                        f"{requested} {interaction.user}",
                        interaction.user.display_avatar,
                        interaction.guild.id,
                    )
                )

    @application_checks.bot_has_guild_permissions(manage_guild=True)
    @application_checks.has_permissions(manage_guild=True)
    @__automod.subcommand(
        name="word_add",
        description="Add word to automoderation",
        name_localizations=get_localized_name("automod_word_add"),
        description_localizations=get_localized_description("automod_word_add"),
    )
    async def __test_automod_wordadd(
        self, interaction: Interaction, word: Optional[str] = SlashOption(required=True)
    ):
        moderation_mode = get_server_moderation_mode(interaction.guild.id)
        if moderation_mode == "friends_group":
            mod_words = fetchall_mod_words(interaction.guild.id)
            if word not in mod_words:
                write_in_mod_word(interaction.guild.id, word)
                message = get_msg_from_locale_by_key(
                    interaction.guild.id,
                    f"automod_{interaction.application_command.name}",
                )
                requested = get_msg_from_locale_by_key(
                    interaction.guild.id, "requested_by"
                )
                await interaction.response.send_message(
                    embed=construct_basic_embed(
                        f"automod_{interaction.application_command.name}",
                        f"{message} **{word}**",
                        f"{requested} {interaction.user}",
                        interaction.user.display_avatar,
                        interaction.guild.id,
                    )
                )
            else:
                message = get_msg_from_locale_by_key(
                    interaction.guild.id, f"already_in_list"
                )
                requested = get_msg_from_locale_by_key(
                    interaction.guild.id, "requested_by"
                )
                await interaction.response.send_message(
                    embed=construct_basic_embed(
                        f"automod_{interaction.application_command.name}",
                        f"{message}",
                        f"{requested} {interaction.user}",
                        interaction.user.display_avatar,
                        interaction.guild.id,
                    )
                )
        elif moderation_mode == "community":
            try:
                auto_mod_rules = await interaction.guild.auto_moderation_rules()
                try:
                    aurora_automoderation_rule = nextcord.utils.get(
                        auto_mod_rules, name="Aurora-Automoderation"
                    )
                    keyword_filter = (
                        aurora_automoderation_rule.trigger_metadata.keyword_filter
                    )
                    if word not in keyword_filter:
                        keyword_filter.append(word)
                        await aurora_automoderation_rule.edit(
                            trigger_metadata=AutoModerationTriggerMetadata(
                                keyword_filter=keyword_filter
                            ),
                            enabled=True,
                        )
                        message = get_msg_from_locale_by_key(
                            interaction.guild.id,
                            f"automod_{interaction.application_command.name}",
                        )
                        requested = get_msg_from_locale_by_key(
                            interaction.guild.id, "requested_by"
                        )
                        await interaction.response.send_message(
                            embed=construct_basic_embed(
                                f"automod_{interaction.application_command.name}",
                                f"{message} **{word}**",
                                f"{requested} {interaction.user}",
                                interaction.user.display_avatar,
                                interaction.guild.id,
                            )
                        )
                    else:
                        message = get_msg_from_locale_by_key(
                            interaction.guild.id, f"already_in_list"
                        )
                        requested = get_msg_from_locale_by_key(
                            interaction.guild.id, "requested_by"
                        )
                        await interaction.response.send_message(
                            embed=construct_basic_embed(
                                f"automod_{interaction.application_command.name}",
                                f"{message}",
                                f"{requested} {interaction.user}",
                                interaction.user.display_avatar,
                                interaction.guild.id,
                            )
                        )
                except Exception as error:
                    print(error)
            except nextcord.Forbidden:
                embed = nextcord.Embed(
                    color=DEFAULT_BOT_COLOR,
                    description=f"{get_msg_from_locale_by_key(interaction.guild.id, 'only_community')}",
                )
                return await interaction.response.send_message(embed=embed)
            except nextcord.NotFound:
                return await interaction.response.send_message(
                    embed=construct_error_not_found_embed(
                        get_msg_from_locale_by_key(
                            interaction.guild.id, "not_found_error"
                        ),
                        self.client.user.avatar.url,
                    )
                )

    @application_checks.bot_has_guild_permissions(manage_guild=True)
    @application_checks.has_permissions(manage_guild=True)
    @__automod.subcommand(
        name="word_remove",
        description="Remove word from automod database",
        name_localizations=get_localized_name("automod_word_remove"),
        description_localizations=get_localized_description("automod_word_remove"),
    )
    async def __test_automod_wordremove(
        self, interaction: Interaction, word: Optional[str] = SlashOption(required=True)
    ):
        moderation_mode = get_server_moderation_mode(interaction.guild.id)
        if moderation_mode == "friends_group":
            mod_words = fetchall_mod_words(interaction.guild.id)
            if word in mod_words:
                delete_mod_word(interaction.guild.id, word)
                message = get_msg_from_locale_by_key(
                    interaction.guild.id,
                    f"automod_{interaction.application_command.name}",
                )
                requested = get_msg_from_locale_by_key(
                    interaction.guild.id, "requested_by"
                )
                await interaction.response.send_message(
                    embed=construct_basic_embed(
                        f"automod_{interaction.application_command.name}",
                        f"{message} **{word}**",
                        f"{requested} {interaction.user}",
                        interaction.user.display_avatar,
                        interaction.guild.id,
                    )
                )
            else:
                message = get_msg_from_locale_by_key(
                    interaction.guild.id, f"already_not_in_list"
                )
                requested = get_msg_from_locale_by_key(
                    interaction.guild.id, "requested_by"
                )
                await interaction.response.send_message(
                    embed=construct_basic_embed(
                        f"automod_{interaction.application_command.name}",
                        f"{message}",
                        f"{requested} {interaction.user}",
                        interaction.user.display_avatar,
                        interaction.guild.id,
                    )
                )
        elif moderation_mode == "community":
            try:
                auto_mod_rules = await interaction.guild.auto_moderation_rules()
                try:
                    aurora_automoderation_rule = nextcord.utils.get(
                        auto_mod_rules, name="Aurora-Automoderation"
                    )
                    keyword_filter = (
                        aurora_automoderation_rule.trigger_metadata.keyword_filter
                    )
                    try:
                        keyword_filter.remove(word)
                    except ValueError:
                        message = get_msg_from_locale_by_key(
                            interaction.guild.id, f"already_not_in_list"
                        )
                        requested = get_msg_from_locale_by_key(
                            interaction.guild.id, "requested_by"
                        )
                        return await interaction.response.send_message(
                            embed=construct_basic_embed(
                                f"automod_{interaction.application_command.name}",
                                f"{message}",
                                f"{requested} {interaction.user}",
                                interaction.user.display_avatar,
                                interaction.guild.id,
                            )
                        )
                    await aurora_automoderation_rule.edit(
                        trigger_metadata=AutoModerationTriggerMetadata(
                            keyword_filter=keyword_filter
                        ),
                        enabled=True,
                    )
                    message = get_msg_from_locale_by_key(
                        interaction.guild.id,
                        f"automod_{interaction.application_command.name}",
                    )
                    requested = get_msg_from_locale_by_key(
                        interaction.guild.id, "requested_by"
                    )
                    await interaction.response.send_message(
                        embed=construct_basic_embed(
                            f"automod_{interaction.application_command.name}",
                            f"{message} **{word}**",
                            f"{requested} {interaction.user}",
                            interaction.user.display_avatar,
                            interaction.guild.id,
                        )
                    )
                except Exception as error:
                    print(error)
            except nextcord.Forbidden:
                embed = nextcord.Embed(
                    color=DEFAULT_BOT_COLOR,
                    description=f"{get_msg_from_locale_by_key(interaction.guild.id, 'only_community')}",
                )
                return await interaction.response.send_message(embed=embed)
            except nextcord.NotFound:
                return await interaction.response.send_message(
                    embed=construct_error_not_found_embed(
                        get_msg_from_locale_by_key(
                            interaction.guild.id, "not_found_error"
                        ),
                        self.client.user.avatar.url,
                    )
                )

    @application_checks.bot_has_guild_permissions(manage_guild=True)
    @application_checks.has_permissions(manage_guild=True)
    @__automod.subcommand(
        name="exempt_role_add",
        description="Added exempt role to automoderation",
        name_localizations=get_localized_name("automod_exempt_role_add"),
        description_localizations=get_localized_description("automod_exempt_role_add"),
    )
    async def __test_automod_exempt_role_add(
        self,
        interaction: Interaction,
        role: Optional[nextcord.Role] = SlashOption(required=True),
    ):

        try:
            auto_mod_rules = await interaction.guild.auto_moderation_rules()
            try:
                aurora_automoderation_rule = nextcord.utils.get(
                    auto_mod_rules, name="Aurora-Automoderation"
                )
                exempt_roles = aurora_automoderation_rule.exempt_roles
                if role not in exempt_roles:
                    exempt_roles.append(role)
                    await aurora_automoderation_rule.edit(
                        exempt_roles=exempt_roles, enabled=True
                    )
                    message = get_msg_from_locale_by_key(
                        interaction.guild.id,
                        f"automod_{interaction.application_command.name}",
                    )
                    requested = get_msg_from_locale_by_key(
                        interaction.guild.id, "requested_by"
                    )
                    await interaction.response.send_message(
                        embed=construct_basic_embed(
                            f"automod_{interaction.application_command.name}",
                            f"{message} {role.mention}",
                            f"{requested} {interaction.user}",
                            interaction.user.display_avatar,
                            interaction.guild.id,
                        )
                    )
                else:
                    message = get_msg_from_locale_by_key(
                        interaction.guild.id, f"already_in_list"
                    )
                    requested = get_msg_from_locale_by_key(
                        interaction.guild.id, "requested_by"
                    )
                    await interaction.response.send_message(
                        embed=construct_basic_embed(
                            f"automod_{interaction.application_command.name}",
                            f"{message}",
                            f"{requested} {interaction.user}",
                            interaction.user.display_avatar,
                            interaction.guild.id,
                        )
                    )
            except Exception as error:
                print(error)
        except nextcord.Forbidden:
            embed = nextcord.Embed(
                color=DEFAULT_BOT_COLOR,
                description=f"{get_msg_from_locale_by_key(interaction.guild.id, 'only_community')}",
            )
            return await interaction.response.send_message(embed=embed)
        except nextcord.NotFound:
            return await interaction.response.send_message(
                embed=construct_error_not_found_embed(
                    get_msg_from_locale_by_key(interaction.guild.id, "not_found_error"),
                    self.client.user.avatar.url,
                )
            )

    @application_checks.bot_has_guild_permissions(manage_guild=True)
    @application_checks.has_permissions(manage_guild=True)
    @__automod.subcommand(
        name="exempt_role_remove",
        description="Removed exempt role from automoderation",
        name_localizations=get_localized_name("automod_exempt_role_remove"),
        description_localizations=get_localized_description(
            "automod_exempt_role_remove"
        ),
    )
    async def __test_automod_exempt_role_remove(
        self,
        interaction: Interaction,
        role: Optional[nextcord.Role] = SlashOption(required=True),
    ):
        try:
            auto_mod_rules = await interaction.guild.auto_moderation_rules()
            try:
                aurora_automoderation_rule = nextcord.utils.get(
                    auto_mod_rules, name="Aurora-Automoderation"
                )
                exempt_roles = aurora_automoderation_rule.exempt_roles
                try:
                    exempt_roles.remove(role)
                except ValueError:
                    message = get_msg_from_locale_by_key(
                        interaction.guild.id, f"already_not_in_list"
                    )
                    requested = get_msg_from_locale_by_key(
                        interaction.guild.id, "requested_by"
                    )
                    return await interaction.response.send_message(
                        embed=construct_basic_embed(
                            f"automod_{interaction.application_command.name}",
                            f"{message}",
                            f"{requested} {interaction.user}",
                            interaction.user.display_avatar,
                            interaction.guild.id,
                        )
                    )
                await aurora_automoderation_rule.edit(
                    exempt_roles=exempt_roles, enabled=True
                )
                message = get_msg_from_locale_by_key(
                    interaction.guild.id,
                    f"automod_{interaction.application_command.name}",
                )
                requested = get_msg_from_locale_by_key(
                    interaction.guild.id, "requested_by"
                )
                await interaction.response.send_message(
                    embed=construct_basic_embed(
                        f"automod_{interaction.application_command.name}",
                        f"{message} {role.mention}",
                        f"{requested} {interaction.user}",
                        interaction.user.display_avatar,
                        interaction.guild.id,
                    )
                )
            except Exception as error:
                print(error)
        except nextcord.Forbidden:
            embed = nextcord.Embed(
                color=DEFAULT_BOT_COLOR,
                description=f"{get_msg_from_locale_by_key(interaction.guild.id, 'only_community')}",
            )
            return await interaction.response.send_message(embed=embed)
        except nextcord.NotFound:
            return await interaction.response.send_message(
                embed=construct_error_not_found_embed(
                    get_msg_from_locale_by_key(interaction.guild.id, "not_found_error"),
                    self.client.user.avatar.url,
                )
            )

    @application_checks.bot_has_guild_permissions(manage_guild=True)
    @application_checks.has_permissions(manage_guild=True)
    @__automod.subcommand(
        name="exempt_channel_add",
        description="Add new exempt channel to automoderation",
        name_localizations=get_localized_name("automod_exempt_channel_add"),
        description_localizations=get_localized_description(
            "automod_exempt_channel_add"
        ),
    )
    async def __test_automod_exempt_channel_add(
        self,
        interaction: Interaction,
        channel: Optional[GuildChannel] = SlashOption(required=True),
    ):
        try:
            auto_mod_rules = await interaction.guild.auto_moderation_rules()
            try:
                aurora_automoderation_rule = nextcord.utils.get(
                    auto_mod_rules, name="Aurora-Automoderation"
                )
                exempt_channels = aurora_automoderation_rule.exempt_channels
                if channel not in exempt_channels:
                    exempt_channels.append(channel)
                    await aurora_automoderation_rule.edit(
                        exempt_channels=exempt_channels, enabled=True
                    )
                    message = get_msg_from_locale_by_key(
                        interaction.guild.id,
                        f"automod_{interaction.application_command.name}",
                    )
                    requested = get_msg_from_locale_by_key(
                        interaction.guild.id, "requested_by"
                    )
                    await interaction.response.send_message(
                        embed=construct_basic_embed(
                            f"automod_{interaction.application_command.name}",
                            f"{message} {channel.mention}",
                            f"{requested} {interaction.user}",
                            interaction.user.display_avatar,
                            interaction.guild.id,
                        )
                    )
                else:
                    message = get_msg_from_locale_by_key(
                        interaction.guild.id, f"already_in_list"
                    )
                    requested = get_msg_from_locale_by_key(
                        interaction.guild.id, "requested_by"
                    )
                    return await interaction.response.send_message(
                        embed=construct_basic_embed(
                            f"automod_{interaction.application_command.name}",
                            f"{message}",
                            f"{requested} {interaction.user}",
                            interaction.user.display_avatar,
                            interaction.guild.id,
                        )
                    )
            except Exception as error:
                print(error)
        except nextcord.Forbidden:
            embed = nextcord.Embed(
                color=DEFAULT_BOT_COLOR,
                description=f"{get_msg_from_locale_by_key(interaction.guild.id, 'only_community')}",
            )
            return await interaction.response.send_message(embed=embed)
        except nextcord.NotFound:
            return await interaction.response.send_message(
                embed=construct_error_not_found_embed(
                    get_msg_from_locale_by_key(interaction.guild.id, "not_found_error"),
                    self.client.user.avatar.url,
                )
            )

    @application_checks.bot_has_guild_permissions(manage_guild=True)
    @application_checks.has_permissions(manage_guild=True)
    @__automod.subcommand(
        name="exempt_channel_remove",
        description="Remove exempt channel from automoderation",
        name_localizations=get_localized_name("automod_exempt_channel_remove"),
        description_localizations=get_localized_description(
            "automod_exempt_channel_remove"
        ),
    )
    async def __test_automod_exempt_channel_remove(
        self,
        interaction: Interaction,
        channel: Optional[GuildChannel] = SlashOption(required=True),
    ):
        try:
            auto_mod_rules = await interaction.guild.auto_moderation_rules()
            try:
                aurora_automoderation_rule = nextcord.utils.get(
                    auto_mod_rules, name="Aurora-Automoderation"
                )
                exempt_channels = aurora_automoderation_rule.exempt_channels
                try:
                    exempt_channels.remove(channel)
                except ValueError:
                    message = get_msg_from_locale_by_key(
                        interaction.guild.id, f"already_not_in_list"
                    )
                    requested = get_msg_from_locale_by_key(
                        interaction.guild.id, "requested_by"
                    )
                    return await interaction.response.send_message(
                        embed=construct_basic_embed(
                            f"automod_{interaction.application_command.name}",
                            f"{message}",
                            f"{requested} {interaction.user}",
                            interaction.user.display_avatar,
                            interaction.guild.id,
                        )
                    )
                await aurora_automoderation_rule.edit(
                    exempt_channels=exempt_channels, enabled=True
                )
                message = get_msg_from_locale_by_key(
                    interaction.guild.id,
                    f"automod_{interaction.application_command.name}",
                )
                requested = get_msg_from_locale_by_key(
                    interaction.guild.id, "requested_by"
                )
                await interaction.response.send_message(
                    embed=construct_basic_embed(
                        f"automod_{interaction.application_command.name}",
                        f"{message} {channel.mention}",
                        f"{requested} {interaction.user}",
                        interaction.user.display_avatar,
                        interaction.guild.id,
                    )
                )
            except Exception as error:
                print(error)
        except nextcord.Forbidden:
            embed = nextcord.Embed(
                color=DEFAULT_BOT_COLOR,
                description=f"{get_msg_from_locale_by_key(interaction.guild.id, 'only_community')}",
            )
            return await interaction.response.send_message(embed=embed)
        except nextcord.NotFound:
            return await interaction.response.send_message(
                embed=construct_error_not_found_embed(
                    get_msg_from_locale_by_key(interaction.guild.id, "not_found_error"),
                    self.client.user.avatar.url,
                )
            )

    @application_checks.bot_has_guild_permissions(kick_members=True)
    @application_checks.has_permissions(manage_guild=True)
    @__automod.subcommand(
        name="nickname_detect",
    )
    async def __test_automod_nickname_detect(
        self,
        interaction: Interaction,
        enable: Optional[bool] = SlashOption(required=True),
    ):
        update_server_nickname_detect(interaction.guild.id, enable)
        message = get_msg_from_locale_by_key(
            interaction.guild.id, f"automod_{interaction.application_command.name}"
        )
        requested = get_msg_from_locale_by_key(interaction.guild.id, "requested_by")
        if enable is True:
            enable = get_msg_from_locale_by_key(interaction.guild.id, "enabled")
        else:
            enable = get_msg_from_locale_by_key(interaction.guild.id, "disabled")
        await interaction.response.send_message(
            embed=construct_basic_embed(
                f"automod_{interaction.application_command.name}",
                f"{message} **{enable}**",
                f"{requested} {interaction.user}",
                interaction.user.display_avatar,
                interaction.guild.id,
            )
        )

    @application_checks.bot_has_guild_permissions(kick_members=True)
    @application_checks.has_permissions(manage_guild=True)
    @__automod.subcommand(
        name="enable",
        description="Turn on/off automod on your server",
        name_localizations=get_localized_name("automod_enable"),
        description_localizations=get_localized_description("automod_enable"),
    )
    async def __test_automod_word_detect(
        self,
        interaction: Interaction,
        enable: Optional[bool] = SlashOption(required=True),
    ):
        update_server_word_detect(interaction.guild.id, enable)
        message = get_msg_from_locale_by_key(
            interaction.guild.id, f"automod_{interaction.application_command.name}"
        )
        requested = get_msg_from_locale_by_key(interaction.guild.id, "requested_by")
        enabled = enable
        if enable is True:
            enable = get_msg_from_locale_by_key(interaction.guild.id, "enabled")
        else:
            enable = get_msg_from_locale_by_key(interaction.guild.id, "disabled")
        await interaction.response.send_message(
            embed=construct_basic_embed(
                f"automod_{interaction.application_command.name}",
                f"{message} **{enable}**",
                f"{requested} {interaction.user}",
                interaction.user.display_avatar,
                interaction.guild.id,
            )
        )
        moderation_mode = get_server_moderation_mode(interaction.guild.id)
        if moderation_mode == "community":
            try:
                auto_mod_rules = await interaction.guild.auto_moderation_rules()
                try:
                    aurora_automoderation_rule = nextcord.utils.get(
                        auto_mod_rules, name="Aurora-Automoderation"
                    )
                    await aurora_automoderation_rule.edit(enabled=enabled)
                except:
                    pass
            except:
                pass

    @application_checks.bot_has_guild_permissions(kick_members=True)
    @application_checks.has_permissions(manage_guild=True)
    @__automod.subcommand(
        name="description_detect",
        description="Turn on/Turn off automoderating newcomers status description",
        name_localizations=get_localized_name("automod_description_detect"),
        description_localizations=get_localized_description(
            "automod_description_detect"
        ),
    )
    async def __test_automod_description_detect(
        self,
        interaction: Interaction,
        enable: Optional[bool] = SlashOption(required=True),
    ):
        update_server_status_detect(interaction.guild.id, enable)
        message = get_msg_from_locale_by_key(
            interaction.guild.id, f"automod_{interaction.application_command.name}"
        )
        requested = get_msg_from_locale_by_key(interaction.guild.id, "requested_by")
        if enable is True:
            enable = get_msg_from_locale_by_key(interaction.guild.id, "enabled")
        else:
            enable = get_msg_from_locale_by_key(interaction.guild.id, "disabled")
        await interaction.response.send_message(
            embed=construct_basic_embed(
                f"automod_{interaction.application_command.name}",
                f"{message} **{enable}**",
                f"{requested} {interaction.user}",
                interaction.user.display_avatar,
                interaction.guild.id,
            )
        )

    @application_checks.bot_has_guild_permissions(kick_members=True)
    @application_checks.has_permissions(manage_guild=True)
    @__automod.subcommand(
        name="link_detect",
        description="Turn on/Turn off automoderating chat for links",
        name_localizations=get_localized_name("automod_link_detect"),
        description_localizations=get_localized_description("automod_link_detect"),
    )
    async def __test_automod_link_detect(
        self,
        interaction: Interaction,
        enable: Optional[bool] = SlashOption(required=True),
    ):
        moderation_mode = get_server_moderation_mode(interaction.guild.id)
        if moderation_mode == "friends_group":
            update_server_link_detect(interaction.guild.id, enable)
            message = get_msg_from_locale_by_key(
                interaction.guild.id, f"automod_{interaction.application_command.name}"
            )
            requested = get_msg_from_locale_by_key(interaction.guild.id, "requested_by")
            if enable is True:
                enable = get_msg_from_locale_by_key(interaction.guild.id, "enabled")
            else:
                enable = get_msg_from_locale_by_key(interaction.guild.id, "disabled")
            await interaction.response.send_message(
                embed=construct_basic_embed(
                    f"automod_{interaction.application_command.name}",
                    f"{message} **{enable}**",
                    f"{requested} {interaction.user}",
                    interaction.user.display_avatar,
                    interaction.guild.id,
                )
            )
        elif moderation_mode == "community":
            try:
                auto_mod_rules = await interaction.guild.auto_moderation_rules()
                try:
                    aurora_automoderation_rule = nextcord.utils.get(
                        auto_mod_rules, name="Aurora-Automoderation"
                    )
                    keyword_filter = (
                        aurora_automoderation_rule.trigger_metadata.keyword_filter
                    )
                    if enable is True:
                        for i in block_links:
                            if i not in keyword_filter:
                                keyword_filter.append(i)
                    if enable is False:
                        try:
                            for i in block_links:
                                keyword_filter.remove(i)
                        except ValueError as error:
                            print(error)
                    await aurora_automoderation_rule.edit(
                        trigger_metadata=AutoModerationTriggerMetadata(
                            keyword_filter=keyword_filter, allow_list=allow_list
                        ),
                        enabled=True,
                    )
                    message = get_msg_from_locale_by_key(
                        interaction.guild.id,
                        f"automod_{interaction.application_command.name}",
                    )
                    requested = get_msg_from_locale_by_key(
                        interaction.guild.id, "requested_by"
                    )
                    if enable is True:
                        enable = get_msg_from_locale_by_key(
                            interaction.guild.id, "enabled"
                        )
                    else:
                        enable = get_msg_from_locale_by_key(
                            interaction.guild.id, "disabled"
                        )
                    await interaction.response.send_message(
                        embed=construct_basic_embed(
                            f"automod_{interaction.application_command.name}",
                            f"{message} **{enable}**",
                            f"{requested} {interaction.user}",
                            interaction.user.display_avatar,
                            interaction.guild.id,
                        )
                    )
                except Exception as error:
                    print(error)
            except nextcord.Forbidden:
                embed = nextcord.Embed(
                    color=DEFAULT_BOT_COLOR,
                    description=f"{get_msg_from_locale_by_key(interaction.guild.id, 'only_community')}",
                )
                return await interaction.response.send_message(embed=embed)
            except nextcord.NotFound:
                return await interaction.response.send_message(
                    embed=construct_error_not_found_embed(
                        get_msg_from_locale_by_key(
                            interaction.guild.id, "not_found_error"
                        ),
                        self.client.user.avatar.url,
                    )
                )

    @application_checks.has_permissions(manage_guild=True)
    @__automod.subcommand(
        name="moderation_mode",
        description="Changes moderation mode on your server",
        name_localizations=get_localized_name("automod_moderation_mode"),
        description_localizations=get_localized_description("automod_moderation_mode"),
    )
    async def __test_automod_moderation_mode(
        self,
        interaction: Interaction,
        moderation_mode: str = SlashOption(
            name="picker",
            choices={"community": "community", "friends_group": "friends_group"},
            required=True,
        ),
    ):
        update_server_moderation_mode(interaction.guild.id, moderation_mode)
        message = get_msg_from_locale_by_key(
            interaction.guild.id, f"automod_{interaction.application_command.name}"
        )
        requested = get_msg_from_locale_by_key(interaction.guild.id, "requested_by")
        await interaction.response.send_message(
            embed=construct_basic_embed(
                f"automod_{interaction.application_command.name}",
                f"{message} **{moderation_mode}**",
                f"{requested} {interaction.user}",
                interaction.user.display_avatar,
                interaction.guild.id,
            )
        )


def setup(client):
    client.add_cog(AutoModeration(client))
