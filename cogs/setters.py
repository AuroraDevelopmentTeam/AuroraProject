import nextcord
from nextcord import Interaction, SlashOption, Permissions
from nextcord.ext import commands, application_checks
from nextcord.abc import GuildChannel

from typing import Optional
from config import settings
import sqlite3

from core.embeds import construct_basic_embed
from core.locales.getters import (
    get_msg_from_locale_by_key,
    get_keys_value_in_locale,
    get_localized_description,
    get_localized_name,
)
from core.money.updaters import (
    update_guild_currency_symbol,
    update_guild_starting_balance,
    update_guild_payday_amount,
    update_user_balance,
)
from core.locales.updaters import update_guild_locale
from core.checkers import is_locale_valid, is_str_or_emoji
from core.levels.updaters import (
    set_server_level_up_messages_state,
    set_user_level,
    update_min_max_exp,
)
from core.welcomers.updaters import (
    set_welcome_channel,
    update_welcome_message_description,
    update_welcome_message_title,
    update_welcome_message_url,
    update_welcome_message_type,
    set_welcome_message_state,
)
from core.goodbyes.updaters import (
    set_goodbye_channel,
    update_goodbye_message_description,
    update_goodbye_message_title,
    update_goodbye_message_url,
    update_goodbye_message_type,
    set_goodbye_message_state,
)
from core.nitro.updaters import (
    set_nitro_channel,
    set_nitro_message_state,
    update_nitro_message_url,
    update_nitro_message_description,
    update_nitro_message_title,
)
from core.loggers.updaters import update_logging_channel_id, update_logging_guild_state
from core.tickets.updaters import (
    update_ticket_archive,
    update_ticket_category,
    update_ticket_support,
)
from core.errors import construct_error_negative_value_embed


class EmbedModal(nextcord.ui.Modal):
    def __init__(self, name):
        self.name = name
        super().__init__(
            "Embed maker",
        )
        self.embedTitle = nextcord.ui.TextInput(
            label="Embed Title",
            min_length=3,
            max_length=248,
            required=True,
            placeholder="Enter the embed's title",
        )
        self.embedDescription = nextcord.ui.TextInput(
            label="Embed Description",
            min_length=5,
            max_length=1900,
            required=True,
            placeholder="Enter the embed's description",
            style=nextcord.TextInputStyle.paragraph,
        )

        self.embedURL = nextcord.ui.TextInput(
            label="Embed's URL",
            min_length=5,
            max_length=250,
            required=True,
            placeholder="Enter the url of image in format: "
            "https://www.example.com/image.png",
        )
        self.add_item(self.embedTitle)
        self.add_item(self.embedDescription)
        self.add_item(self.embedURL)

    async def callback(self, interaction: Interaction) -> None:
        title = self.embedTitle.value
        description = self.embedDescription.value
        url = self.embedURL.value
        if self.name == "welcome":
            update_welcome_message_title(interaction.guild.id, title)
            update_welcome_message_description(interaction.guild.id, description)
            update_welcome_message_url(interaction.guild.id, url)
        elif self.name == "nitro":
            update_nitro_message_title(interaction.guild.id, title)
            update_nitro_message_description(interaction.guild.id, description)
            update_nitro_message_url(interaction.guild.id, url)
        else:
            update_goodbye_message_title(interaction.guild.id, title)
            update_goodbye_message_description(interaction.guild.id, description)
            update_goodbye_message_url(interaction.guild.id, url)
        embed = nextcord.Embed(title=title, description=description)
        embed.set_image(url=url)
        return await interaction.response.send_message(embed=embed)


class Setters(commands.Cog):
    def __init__(self, client):
        self.client = client

    @nextcord.slash_command(
        name="set",
        name_localizations=get_localized_name("set"),
        description_localizations=get_localized_description("set"),
        default_member_permissions=Permissions(administrator=True),
    )
    @application_checks.has_permissions(manage_guild=True)
    async def __set(self, interaction: Interaction):
        """
        This is the set slash command that will be the prefix of set commands.
        """
        pass

    @__set.subcommand(
        name="locale",
        description="Choose bot's respond's main language on your server!",
        name_localizations=get_localized_name("set_locale"),
        description_localizations=get_localized_description("set_locale"),
    )
    async def __locale_set(
        self,
        interaction: Interaction,
        locale: str = SlashOption(
            name="picker",
            choices={"russian": "ru_ru", "english": "en_us"},
            required=True,
        ),
    ):
        """
        Parameters
        ----------
        interaction: Interaction
            The interaction object
        locale: Optional[str]
            Locale is the bot respond language. Available locales: ru_ru/en_us
        """
        if is_locale_valid(locale) is True:
            update_guild_locale(locale, interaction.guild.id)
            message = get_msg_from_locale_by_key(
                interaction.guild.id, f"set_{interaction.application_command.name}"
            )
            requested = get_msg_from_locale_by_key(interaction.guild.id, "requested_by")
            await interaction.response.send_message(
                embed=construct_basic_embed(
                    f"set_{interaction.application_command.name}",
                    f"{message} **{locale}**",
                    f"{requested} {interaction.user}",
                    interaction.user.display_avatar,
                    interaction.guild.id,
                )
            )
        else:
            await interaction.response.send_message("something gone wrong")

    @__set.subcommand(
        name="currency",
        description="Set server's currency to new symbol",
        name_localizations=get_localized_name("set_currency"),
        description_localizations=get_localized_description("set_currency"),
    )
    async def __currency_set(
        self,
        interaction: Interaction,
        currency_symbol: Optional[str] = SlashOption(required=True),
    ):
        """
        Parameters
        ----------
        interaction: Interaction
            The interaction object
        currency_symbol: Optional[str]
            New symbol for currency
        """
        if is_str_or_emoji(currency_symbol):
            update_guild_currency_symbol(interaction.guild.id, currency_symbol)
            message = get_msg_from_locale_by_key(
                interaction.guild.id, f"set_{interaction.application_command.name}"
            )
            requested = get_msg_from_locale_by_key(interaction.guild.id, "requested_by")
            await interaction.response.send_message(
                embed=construct_basic_embed(
                    interaction.application_command.name,
                    f"{message} **{currency_symbol}**",
                    f"{requested} {interaction.user}",
                    interaction.user.display_avatar,
                    interaction.guild.id,
                )
            )
        else:
            await interaction.response.send_message("error")

    @__set.subcommand(
        name="start_balance",
        description="Set's server starting balance to new number",
        name_localizations=get_localized_name("set_start_balance"),
        description_localizations=get_localized_description("set_start_balance"),
    )
    async def __start_balance_set(
        self,
        interaction: Interaction,
        balance: Optional[int] = SlashOption(required=True),
    ):
        """
        Parameters
        ----------
        interaction: Interaction
            The interaction object
        balance: Optional[int]
            New guests of server will start with this number of money on their balance
        """
        if balance >= 0 and isinstance(balance, int):
            update_guild_starting_balance(interaction.guild.id, balance)
            message = get_msg_from_locale_by_key(
                interaction.guild.id, f"set_{interaction.application_command.name}"
            )
            requested = get_msg_from_locale_by_key(interaction.guild.id, "requested_by")
            await interaction.response.send_message(
                embed=construct_basic_embed(
                    interaction.application_command.name,
                    f"{message} **{balance}**",
                    f"{requested} {interaction.user}",
                    interaction.user.display_avatar,
                    interaction.guild.id,
                )
            )
        else:
            await interaction.response.send_message("error")

    @__set.subcommand(
        name="timely_amount",
        description="Set's server payday amount per time with /timely command",
        name_localizations=get_localized_name("set_timely_amount"),
        description_localizations=get_localized_description("set_timely_amount"),
    )
    async def __payday_amount_set(
        self,
        interaction: Interaction,
        payday_amount: Optional[int] = SlashOption(required=True),
    ):
        """
        Parameters
        ----------
        interaction: Interaction
            The interaction object
        payday_amount: Optional[int]
            Members of server will get this number of money on their balance with /timely command
        """
        if payday_amount >= 0 and isinstance(payday_amount, int):
            update_guild_payday_amount(interaction.guild.id, payday_amount)
            message = get_msg_from_locale_by_key(
                interaction.guild.id, f"set_{interaction.application_command.name}"
            )
            requested = get_msg_from_locale_by_key(interaction.guild.id, "requested_by")
            await interaction.response.send_message(
                embed=construct_basic_embed(
                    interaction.application_command.name,
                    f"{message} **{payday_amount}**",
                    f"{requested} {interaction.user}",
                    interaction.user.display_avatar,
                    interaction.guild.id,
                )
            )
        else:
            await interaction.response.send_message("error")

    @__set.subcommand(
        name="level_up_messages",
        description="Turn on or turn off level up messages on your server",
        name_localizations=get_localized_name("set_level_up_messages"),
        description_localizations=get_localized_description("set_level_up_messages"),
    )
    async def __level_up_messages_state(
        self,
        interaction: Interaction,
        level_up_messages_state: int = SlashOption(
            name="picker", choices={"turn on": 1, "turn off": 0}, required=True
        ),
    ):
        level_up_messages_state = bool(level_up_messages_state)
        set_server_level_up_messages_state(
            interaction.guild.id, level_up_messages_state
        )
        message = get_msg_from_locale_by_key(
            interaction.guild.id, f"set_{interaction.application_command.name}"
        )
        requested = get_msg_from_locale_by_key(interaction.guild.id, "requested_by")
        if level_up_messages_state is True:
            level_up_messages_state = get_msg_from_locale_by_key(
                interaction.guild.id, "enabled"
            )
        else:
            level_up_messages_state = get_msg_from_locale_by_key(
                interaction.guild.id, "disabled"
            )
        await interaction.response.send_message(
            embed=construct_basic_embed(
                interaction.application_command.name,
                f"{message} **{level_up_messages_state}**",
                f"{requested} {interaction.user}",
                interaction.user.display_avatar,
                interaction.guild.id,
            )
        )

    @__set.subcommand(
        name="level",
        description="Setting user's level to some integer value",
        name_localizations=get_localized_name("set_level"),
        description_localizations=get_localized_description("set_level"),
    )
    async def __level_set(
        self,
        interaction: Interaction,
        user: Optional[nextcord.Member] = SlashOption(required=True),
        level: Optional[int] = SlashOption(required=True),
    ):
        if level <= 0:
            return await interaction.response.send_message(
                embed=construct_error_negative_value_embed(
                    get_msg_from_locale_by_key(
                        interaction.guild.id, "negative_value_error"
                    ),
                    self.client.user.avatar.url,
                    money,
                )
            )
        set_user_level(interaction.guild.id, user.id, level)
        message = get_msg_from_locale_by_key(
            interaction.guild.id, f"set_{interaction.application_command.name}"
        )
        message_2 = get_msg_from_locale_by_key(
            interaction.guild.id, f"set_{interaction.application_command.name}_2"
        )
        requested = get_msg_from_locale_by_key(interaction.guild.id, "requested_by")
        await interaction.response.send_message(
            embed=construct_basic_embed(
                interaction.application_command.name,
                f"{message} {user.mention} {message_2} __**{level}**__",
                f"{requested} {interaction.user}",
                interaction.user.display_avatar,
                interaction.guild.id,
            )
        )

    @__set.subcommand(
        name="min_max_exp",
        description="Setting server's min and max exp per writed message",
        name_localizations=get_localized_name("set_min_max_exp"),
        description_localizations=get_localized_description("set_min_max_exp"),
    )
    async def __min_max_exp_set(
        self,
        interaction: Interaction,
        min: Optional[int] = SlashOption(required=True),
        max: Optional[int] = SlashOption(required=True),
    ):
        if min < 0:
            return await interaction.response.send_message(
                embed=construct_error_negative_value_embed(
                    get_msg_from_locale_by_key(
                        interaction.guild.id, "negative_value_error"
                    ),
                    self.client.user.avatar.url,
                    money,
                )
            )
        if max < 0:
            return await interaction.response.send_message(
                embed=construct_error_negative_value_embed(
                    get_msg_from_locale_by_key(
                        interaction.guild.id, "negative_value_error"
                    ),
                    self.client.user.avatar.url,
                    money,
                )
            )
        if max < min:
            return await interaction.response.send_message(
                embed=construct_error_negative_value_embed(
                    get_msg_from_locale_by_key(
                        interaction.guild.id, "negative_value_error"
                    ),
                    self.client.user.avatar.url,
                    f"{min} - {max}",
                )
            )
        update_min_max_exp(interaction.guild.id, min, max)
        message = get_msg_from_locale_by_key(
            interaction.guild.id, f"set_{interaction.application_command.name}"
        )
        requested = get_msg_from_locale_by_key(interaction.guild.id, "requested_by")
        await interaction.response.send_message(
            embed=construct_basic_embed(
                interaction.application_command.name,
                f"{message} **{min}** - **{max}**",
                f"{requested} {interaction.user}",
                interaction.user.display_avatar,
                interaction.guild.id,
            )
        )

    @__set.subcommand(
        name="welcome_channel",
        description="Setting server's welcome channel to send welcome messages",
        name_localizations=get_localized_name("set_welcome_channel"),
        description_localizations=get_localized_description("set_welcome_channel"),
    )
    async def welcome_channel_set(
        self,
        interaction: Interaction,
        channel: Optional[GuildChannel] = SlashOption(required=True),
    ):
        """
        Parameters
        ----------
        interaction: Interaction
            The interaction object
        channel: str
            Channel to
        """
        try:
            if isinstance(channel, nextcord.TextChannel):
                set_welcome_channel(interaction.guild.id, channel.id)
                message = get_msg_from_locale_by_key(
                    interaction.guild.id, f"set_{interaction.application_command.name}"
                )
                requested = get_msg_from_locale_by_key(
                    interaction.guild.id, "requested_by"
                )
                await interaction.response.send_message(
                    embed=construct_basic_embed(
                        interaction.application_command.name,
                        f"{message} {channel.mention}",
                        f"{requested} {interaction.user}",
                        interaction.user.display_avatar,
                        interaction.guild.id,
                    )
                )
            else:
                return await interaction.response.send_message(
                    embed=construct_error_negative_value_embed(
                        get_msg_from_locale_by_key(
                            interaction.guild.id, "negative_value_error"
                        ),
                        self.client.user.avatar.url,
                        channel,
                    )
                )
        except AttributeError:
            return await interaction.response.send_message(
                embed=construct_error_negative_value_embed(
                    get_msg_from_locale_by_key(
                        interaction.guild.id, "negative_value_error"
                    ),
                    self.client.user.avatar.url,
                    channel,
                )
            )

    @__set.subcommand(
        name="welcome_embed",
        description="Setting server's welcoming message embed",
        name_localizations=get_localized_name("set_welcome_embed"),
        description_localizations=get_localized_description("set_welcome_embed"),
    )
    async def welcome_embed_set(self, interaction: Interaction):
        modal = EmbedModal("welcome")
        await interaction.response.send_modal(modal)

    @__set.subcommand(
        name="welcome_message_type",
        description="Choose bot's welcome message type on your server!",
        name_localizations=get_localized_name("set_welcome_message_type"),
        description_localizations=get_localized_description("set_welcome_message_type"),
    )
    async def __welcome_message_type_set(
        self,
        interaction: Interaction,
        welcome_message_type: str = SlashOption(
            name="picker",
            choices={
                "Welcome message type: photo card": "card",
                "Welcome message type: embed message": "embed",
            },
            required=True,
        ),
    ):
        """
        Parameters
        ----------
        interaction: Interaction
            The interaction object
        welcome_message_type: Optional[str]
            Avialable types of welcome message are card and embed
        """
        update_welcome_message_type(interaction.guild.id, welcome_message_type)
        message = get_msg_from_locale_by_key(
            interaction.guild.id, f"set_{interaction.application_command.name}"
        )
        requested = get_msg_from_locale_by_key(interaction.guild.id, "requested_by")
        await interaction.response.send_message(
            embed=construct_basic_embed(
                interaction.application_command.name,
                f"{message} **{welcome_message_type}**",
                f"{requested} {interaction.user}",
                interaction.user.display_avatar,
                interaction.guild.id,
            )
        )

    @__set.subcommand(
        name="welcome_message_state",
        description="Turn on or turn off welcome messages on your server",
        name_localizations=get_localized_name("set_welcome_message_state"),
        description_localizations=get_localized_description(
            "set_welcome_message_state"
        ),
    )
    async def __welcome_messages_state_set(
        self,
        interaction: Interaction,
        welcome_message_state: int = SlashOption(
            name="picker", choices={"turn on": 1, "turn off": 0}, required=True
        ),
    ):
        welcome_message_state = bool(welcome_message_state)
        set_welcome_message_state(interaction.guild.id, welcome_message_state)
        message = get_msg_from_locale_by_key(
            interaction.guild.id, f"set_{interaction.application_command.name}"
        )
        requested = get_msg_from_locale_by_key(interaction.guild.id, "requested_by")
        if welcome_message_state is True:
            welcome_message_state = get_msg_from_locale_by_key(
                interaction.guild.id, "enabled"
            )
        else:
            welcome_message_state = get_msg_from_locale_by_key(
                interaction.guild.id, "disabled"
            )
        await interaction.response.send_message(
            embed=construct_basic_embed(
                interaction.application_command.name,
                f"{message} **{welcome_message_state}**",
                f"{requested} {interaction.user}",
                interaction.user.display_avatar,
                interaction.guild.id,
            )
        )

    @__set.subcommand(
        name="goodbye_channel",
        description="Setting server's goodbye channel to send goodbye messages",
        name_localizations=get_localized_name("set_goodbye_channel"),
        description_localizations=get_localized_description("set_goodbye_channel"),
    )
    async def goodbye_channel_set(
        self,
        interaction: Interaction,
        channel: Optional[GuildChannel] = SlashOption(required=True),
    ):
        """
        Parameters
        ----------
        interaction: Interaction
            The interaction object
        channel: str
            Channel to
        """
        if isinstance(channel, nextcord.TextChannel):
            set_goodbye_channel(interaction.guild.id, channel.id)
            message = get_msg_from_locale_by_key(
                interaction.guild.id, f"set_{interaction.application_command.name}"
            )
            requested = get_msg_from_locale_by_key(interaction.guild.id, "requested_by")
            await interaction.response.send_message(
                embed=construct_basic_embed(
                    interaction.application_command.name,
                    f"{message} {channel.mention}",
                    f"{requested} {interaction.user}",
                    interaction.user.display_avatar,
                    interaction.guild.id,
                )
            )
        else:
            return await interaction.response.send_message(
                embed=construct_error_negative_value_embed(
                    get_msg_from_locale_by_key(
                        interaction.guild.id, "negative_value_error"
                    ),
                    self.client.user.avatar.url,
                    channel,
                )
            )

    @__set.subcommand(
        name="goodbye_embed",
        description="Setting server's goodbye message embed",
        name_localizations=get_localized_name("set_goodbye_embed"),
        description_localizations=get_localized_description("set_goodbye_embed"),
    )
    async def goodbye_embed_set(self, interaction: Interaction):
        modal = EmbedModal("goodbye")
        await interaction.response.send_modal(modal)

    @__set.subcommand(
        name="goodbye_message_type",
        description="Choose bot's goodbye message type on your server!",
        name_localizations=get_localized_name("set_goodbye_message_type"),
        description_localizations=get_localized_description("set_goodbye_message_type"),
    )
    async def __goodbye_message_type_set(
        self,
        interaction: Interaction,
        goodbye_message_type: str = SlashOption(
            name="picker",
            choices={
                "goodbye message type: photo card": "card",
                "goodbye message type: embed message": "embed",
            },
            required=True,
        ),
    ):
        """
        Parameters
        ----------
        interaction: Interaction
            The interaction object
        goodbye_message_type: Optional[str]
            Avialable types of goodbye message are card and embed
        """
        update_goodbye_message_type(interaction.guild.id, goodbye_message_type)
        message = get_msg_from_locale_by_key(
            interaction.guild.id, f"set_{interaction.application_command.name}"
        )
        requested = get_msg_from_locale_by_key(interaction.guild.id, "requested_by")
        await interaction.response.send_message(
            embed=construct_basic_embed(
                interaction.application_command.name,
                f"{message} **{goodbye_message_type}**",
                f"{requested} {interaction.user}",
                interaction.user.display_avatar,
                interaction.guild.id,
            )
        )

    @__set.subcommand(
        name="goodbye_message_state",
        description="Turn on or turn off goodbye messages on your server",
        name_localizations=get_localized_name("set_goodbye_message_state"),
        description_localizations=get_localized_description(
            "set_goodbye_message_state"
        ),
    )
    async def __goodbye_messages_state_set(
        self,
        interaction: Interaction,
        goodbye_message_state: int = SlashOption(
            name="picker", choices={"turn on": 1, "turn off": 0}, required=True
        ),
    ):
        goodbye_message_state = bool(goodbye_message_state)
        set_goodbye_message_state(interaction.guild.id, goodbye_message_state)
        message = get_msg_from_locale_by_key(
            interaction.guild.id, f"set_{interaction.application_command.name}"
        )
        requested = get_msg_from_locale_by_key(interaction.guild.id, "requested_by")
        if goodbye_message_state is True:
            goodbye_message_state = get_msg_from_locale_by_key(
                interaction.guild.id, "enabled"
            )
        else:
            goodbye_message_state = get_msg_from_locale_by_key(
                interaction.guild.id, "disabled"
            )
        await interaction.response.send_message(
            embed=construct_basic_embed(
                interaction.application_command.name,
                f"{message} **{goodbye_message_state}**",
                f"{requested} {interaction.user}",
                interaction.user.display_avatar,
                interaction.guild.id,
            )
        )

    @__set.subcommand(
        name="nitro_channel",
        description="Setting server's message channel on nitro boost",
        name_localizations=get_localized_name("set_nitro_channel"),
        description_localizations=get_localized_description("set_nitro_channel"),
    )
    async def __nitro_channel_set(
        self,
        interaction: Interaction,
        channel: Optional[GuildChannel] = SlashOption(required=True),
    ):
        """
        Parameters
        ----------
        interaction: Interaction
            The interaction object
        channel: str
            Channel to
        """
        if isinstance(channel, nextcord.TextChannel):
            set_nitro_channel(interaction.guild.id, channel.id)
            message = get_msg_from_locale_by_key(
                interaction.guild.id, f"set_{interaction.application_command.name}"
            )
            requested = get_msg_from_locale_by_key(interaction.guild.id, "requested_by")
            await interaction.response.send_message(
                embed=construct_basic_embed(
                    interaction.application_command.name,
                    f"{message} {channel.mention}",
                    f"{requested} {interaction.user}",
                    interaction.user.display_avatar,
                    interaction.guild.id,
                )
            )
        else:
            return await interaction.response.send_message(
                embed=construct_error_negative_value_embed(
                    get_msg_from_locale_by_key(
                        interaction.guild.id, "negative_value_error"
                    ),
                    self.client.user.avatar.url,
                    channel,
                )
            )

    @__set.subcommand(
        name="nitro_embed",
        description="Setting server's on nitro boost message embed",
        name_localizations=get_localized_name("set_nitro_embed"),
        description_localizations=get_localized_description("set_nitro_embed"),
    )
    async def __nitro_embed_set(self, interaction: Interaction):
        modal = EmbedModal("nitro")
        await interaction.response.send_modal(modal)

    @__set.subcommand(
        name="nitro_message_state",
        description="Turn on or turn off on nitro boost messages on your " "server",
        name_localizations=get_localized_name("set_nitro_message_state"),
        description_localizations=get_localized_description("set_nitro_message_state"),
    )
    async def __nitro_messages_state_set(
        self,
        interaction: Interaction,
        nitro_message_state: int = SlashOption(
            name="picker", choices={"turn on": 1, "turn off": 0}, required=True
        ),
    ):
        nitro_message_state = bool(nitro_message_state)
        set_nitro_message_state(interaction.guild.id, nitro_message_state)
        message = get_msg_from_locale_by_key(
            interaction.guild.id, f"set_{interaction.application_command.name}"
        )
        requested = get_msg_from_locale_by_key(interaction.guild.id, "requested_by")
        if nitro_message_state is True:
            nitro_message_state = get_msg_from_locale_by_key(
                interaction.guild.id, "enabled"
            )
        else:
            nitro_message_state = get_msg_from_locale_by_key(
                interaction.guild.id, "disabled"
            )
        await interaction.response.send_message(
            embed=construct_basic_embed(
                interaction.application_command.name,
                f"{message} **{nitro_message_state}**",
                f"{requested} {interaction.user}",
                interaction.user.display_avatar,
                interaction.guild.id,
            )
        )

    @__set.subcommand(
        name="logging_channel",
        description="Setting server's logs channel",
        name_localizations=get_localized_name("set_logging_channel"),
        description_localizations=get_localized_description("set_logging_channel"),
    )
    async def __logging_channel_set(
        self,
        interaction: Interaction,
        channel: Optional[GuildChannel] = SlashOption(required=True),
    ):
        if not isinstance(channel, nextcord.TextChannel):
            return await interaction.response.send_message(
                embed=construct_error_negative_value_embed(
                    get_msg_from_locale_by_key(
                        interaction.guild.id, "negative_value_error"
                    ),
                    self.client.user.avatar.url,
                    channel,
                )
            )
        update_logging_channel_id(interaction.guild.id, channel.id)
        message = get_msg_from_locale_by_key(
            interaction.guild.id, f"set_{interaction.application_command.name}"
        )
        requested = get_msg_from_locale_by_key(interaction.guild.id, "requested_by")
        await interaction.response.send_message(
            embed=construct_basic_embed(
                interaction.application_command.name,
                f"{message} {channel.mention}",
                f"{requested} {interaction.user}",
                interaction.user.display_avatar,
                interaction.guild.id,
            )
        )

    @__set.subcommand(
        name="logging_state",
        description="Setting server's logs channel",
        name_localizations=get_localized_name("set_logging_state"),
        description_localizations=get_localized_description("set_logging_state"),
    )
    async def __logging_state_set(
        self,
        interaction: Interaction,
        logging_state: int = SlashOption(
            name="picker", choices={"turn on": 1, "turn off": 0}, required=True
        ),
    ):
        logging_state = bool(logging_state)
        update_logging_guild_state(interaction.guild.id, logging_state)
        message = get_msg_from_locale_by_key(
            interaction.guild.id, f"set_{interaction.application_command.name}"
        )
        requested = get_msg_from_locale_by_key(interaction.guild.id, "requested_by")
        if logging_state is True:
            logging_state = get_msg_from_locale_by_key(interaction.guild.id, "enabled")
        else:
            logging_state = get_msg_from_locale_by_key(interaction.guild.id, "disabled")
        await interaction.response.send_message(
            embed=construct_basic_embed(
                interaction.application_command.name,
                f"{message} **{logging_state}**",
                f"{requested} {interaction.user}",
                interaction.user.display_avatar,
                interaction.guild.id,
            )
        )

    @__set.subcommand(
        name="ticket_category",
        description="set tickets category",
        name_localizations=get_localized_name("set_ticket_category"),
        description_localizations=get_localized_description("set_ticket_category"),
    )
    async def __ticket_category_set(
        self,
        interaction: Interaction,
        ticket_category_id: Optional[str] = SlashOption(required=True),
    ):
        try:
            ticket_category_id = int(ticket_category_id)
        except ValueError:
            return await interaction.response.send_message(
                embed=construct_error_negative_value_embed(
                    get_msg_from_locale_by_key(
                        interaction.guild.id, "negative_value_error"
                    ),
                    self.client.user.avatar.url,
                    money,
                )
            )
        if not isinstance(ticket_category_id, int):
            return await interaction.response.send_message(
                embed=construct_error_negative_value_embed(
                    get_msg_from_locale_by_key(
                        interaction.guild.id, "negative_value_error"
                    ),
                    self.client.user.avatar.url,
                    money,
                )
            )
        try:
            category = nextcord.utils.get(
                interaction.guild.categories, id=ticket_category_id
            )
            update_ticket_category(interaction.guild.id, category.id)
            message = get_msg_from_locale_by_key(
                interaction.guild.id, f"set_{interaction.application_command.name}"
            )
            requested = get_msg_from_locale_by_key(interaction.guild.id, "requested_by")
            await interaction.response.send_message(
                embed=construct_basic_embed(
                    interaction.application_command.name,
                    f"{message} {category.mention}",
                    f"{requested} {interaction.user}",
                    interaction.user.display_avatar,
                    interaction.guild.id,
                )
            )
        except:
            return

    @__set.subcommand(
        name="ticket_archive",
        description="set tickets archive category",
        name_localizations=get_localized_name("set_ticket_archive"),
        description_localizations=get_localized_description("set_ticket_archive"),
    )
    async def __ticket_archive_set(
        self,
        interaction: Interaction,
        ticket_category_id: Optional[str] = SlashOption(required=True),
    ):
        try:
            ticket_category_id = int(ticket_category_id)
        except ValueError:
            return await interaction.response.send_message(
                embed=construct_error_negative_value_embed(
                    get_msg_from_locale_by_key(
                        interaction.guild.id, "negative_value_error"
                    ),
                    self.client.user.avatar.url,
                    money,
                )
            )
        if not isinstance(ticket_category_id, int):
            return await interaction.response.send_message(
                embed=construct_error_negative_value_embed(
                    get_msg_from_locale_by_key(
                        interaction.guild.id, "negative_value_error"
                    ),
                    self.client.user.avatar.url,
                    money,
                )
            )
        try:
            category = nextcord.utils.get(
                interaction.guild.categories, id=ticket_category_id
            )
            update_ticket_archive(interaction.guild.id, category.id)
            message = get_msg_from_locale_by_key(
                interaction.guild.id, f"set_{interaction.application_command.name}"
            )
            requested = get_msg_from_locale_by_key(interaction.guild.id, "requested_by")
            await interaction.response.send_message(
                embed=construct_basic_embed(
                    interaction.application_command.name,
                    f"{message} {category.mention}",
                    f"{requested} {interaction.user}",
                    interaction.user.display_avatar,
                    interaction.guild.id,
                )
            )
        except:
            return

    @__set.subcommand(
        name="ticket_support",
        description="set tickets archive category",
        name_localizations=get_localized_name("set_ticket_support"),
        description_localizations=get_localized_description("set_ticket_support"),
    )
    async def __ticket_support_set(
        self,
        interaction: Interaction,
        ticket_support: Optional[nextcord.Role] = SlashOption(required=True),
    ):
        update_ticket_support(interaction.guild.id, ticket_support.id)
        message = get_msg_from_locale_by_key(
            interaction.guild.id, f"set_{interaction.application_command.name}"
        )
        requested = get_msg_from_locale_by_key(interaction.guild.id, "requested_by")
        await interaction.response.send_message(
            embed=construct_basic_embed(
                interaction.application_command.name,
                f"{message} {ticket_support.mention}",
                f"{requested} {interaction.user}",
                interaction.user.display_avatar,
                interaction.guild.id,
            )
        )


def setup(client):
    client.add_cog(Setters(client))
