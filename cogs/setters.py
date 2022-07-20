import nextcord
from nextcord import Interaction, SlashOption
from nextcord.ext import commands

from typing import Optional
from config import settings
import sqlite3

from core.embeds import construct_basic_embed
from core.locales.getters import get_msg_from_locale_by_key, get_keys_value_in_locale
from core.money.updaters import update_guild_currency_symbol, update_guild_starting_balance, \
    update_guild_payday_amount, update_user_balance
from core.locales.updaters import update_guild_locale
from core.checkers import is_locale_valid, is_str_or_emoji
from core.levels.updaters import set_server_level_up_messages_state, set_user_level
from core.welcomers.updaters import set_welcome_channel, update_welcome_message_description, \
    update_welcome_message_title, update_welcome_message_url, update_welcome_message_type


class EmbedModal(nextcord.ui.Modal):
    def __init__(self):
        super().__init__(
            "Embed maker",
        )
        self.embedTitle = nextcord.ui.TextInput(label="Embed Title", min_length=3, max_length=248,
                                                required=True, placeholder="Enter the embed's title")
        self.embedDescription = nextcord.ui.TextInput(label="Embed Description", min_length=5, max_length=1900,
                                                      required=True, placeholder="Enter the embed's description",
                                                      style=nextcord.TextInputStyle.paragraph)

        self.embedURL = nextcord.ui.TextInput(label="Embed's URL", min_length=5, max_length=250,
                                              required=True, placeholder="Enter the url of image in format: "
                                                                         "https://www.example.com/image.png")
        self.add_item(self.embedTitle)
        self.add_item(self.embedDescription)
        self.add_item(self.embedURL)

    async def callback(self, interaction: Interaction) -> None:
        title = self.embedTitle.value
        update_welcome_message_title(interaction.guild.id, title)
        description = self.embedDescription.value
        update_welcome_message_description(interaction.guild.id, description)
        url = self.embedURL.value
        update_welcome_message_url(interaction.guild.id, url)
        embed = nextcord.Embed(title=title, description=description)
        embed.set_image(url=url)
        return await interaction.response.send_message(embed=embed)


class Setters(commands.Cog):
    def __init__(self, client):
        self.client = client

    @nextcord.slash_command(name="set")
    async def __set(self, interaction: Interaction):
        """
        This is the set slash command that will be the prefix of economical set commands below.
        """
        pass

    @__set.subcommand(name='locale', description="Choose bot's respond's main language on your server!")
    async def __locale_set(self, interaction: Interaction, locale: str = SlashOption(
        name="picker",
        choices={"russian": "ru_ru", "english": "en_us"},
        required=True
    )):
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
            message = get_msg_from_locale_by_key(interaction.guild.id, f"set_{interaction.application_command.name}")
            requested = get_msg_from_locale_by_key(interaction.guild.id, 'requested_by')
            await interaction.response.send_message(
                embed=construct_basic_embed(interaction.application_command.name,
                                            f"{message} **{locale}**",
                                            f"{requested} {interaction.user}",
                                            interaction.user.display_avatar))
        else:
            await interaction.response.send_message('something gone wrong')

    @__set.subcommand(name="currency", description="Set server's currency to new symbol")
    async def __currency_set(self, interaction: Interaction,
                             currency_symbol: Optional[str] = SlashOption(required=True)):
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
            message = get_msg_from_locale_by_key(interaction.guild.id, f"set_{interaction.application_command.name}")
            requested = get_msg_from_locale_by_key(interaction.guild.id, 'requested_by')
            await interaction.response.send_message(
                embed=construct_basic_embed(interaction.application_command.name,
                                            f"{message} **{currency_symbol}**",
                                            f"{requested} {interaction.user}",
                                            interaction.user.display_avatar))
        else:
            await interaction.response.send_message('error')

    @__set.subcommand(name="start_balance", description="Set's server starting balance to new number")
    async def __start_balance_set(self, interaction: Interaction, balance: Optional[int] = SlashOption(required=True)):
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
            message = get_msg_from_locale_by_key(interaction.guild.id, f"set_{interaction.application_command.name}")
            requested = get_msg_from_locale_by_key(interaction.guild.id, 'requested_by')
            await interaction.response.send_message(
                embed=construct_basic_embed(interaction.application_command.name,
                                            f"{message} **{balance}**",
                                            f"{requested} {interaction.user}",
                                            interaction.user.display_avatar))
        else:
            await interaction.response.send_message('error')

    @__set.subcommand(name="timely_amount", description="Set's server payday amount per time with /timely "
                                                        "command")
    async def __payday_amount_set(self, interaction: Interaction,
                                  payday_amount: Optional[int] = SlashOption(required=True)):
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
            message = get_msg_from_locale_by_key(interaction.guild.id, f"set_{interaction.application_command.name}")
            requested = get_msg_from_locale_by_key(interaction.guild.id, 'requested_by')
            await interaction.response.send_message(
                embed=construct_basic_embed(interaction.application_command.name,
                                            f"{message} **{payday_amount}**",
                                            f"{requested} {interaction.user}",
                                            interaction.user.display_avatar))
        else:
            await interaction.response.send_message('error')

    @__set.subcommand(name="level_up_messages", description="Turn on or turn off level up messages on your server")
    async def __level_up_messages_state(self, interaction: Interaction, level_up_messages_state: int = SlashOption(
        name="picker",
        choices={"turn on": 1, "turn off": 0},
        required=True
    )):
        set_server_level_up_messages_state(interaction.guild.id, bool(level_up_messages_state))
        message = get_msg_from_locale_by_key(interaction.guild.id, f"set_{interaction.application_command.name}")
        requested = get_msg_from_locale_by_key(interaction.guild.id, 'requested_by')
        if level_up_messages_state is True:
            level_up_messages_state = "enabled"
        else:
            level_up_messages_state = "disabled"
        await interaction.response.send_message(
            embed=construct_basic_embed(interaction.application_command.name,
                                        f"{message} **{level_up_messages_state}**",
                                        f"{requested} {interaction.user}",
                                        interaction.user.display_avatar))

    @__set.subcommand(name="level", description="Setting user's level to some integer value")
    async def __level_set(self, interaction: Interaction, user: Optional[nextcord.Member] = SlashOption(required=True),
                          level: Optional[int] = SlashOption(required=True)):
        set_user_level(interaction.guild.id, user.id, level)
        message = get_msg_from_locale_by_key(interaction.guild.id, f"set_{interaction.application_command.name}")
        message_2 = get_msg_from_locale_by_key(interaction.guild.id, f"set_{interaction.application_command.name}_2")
        requested = get_msg_from_locale_by_key(interaction.guild.id, 'requested_by')
        await interaction.response.send_message(
            embed=construct_basic_embed(interaction.application_command.name,
                                        f"{message} {user.mention} {message_2} __**{level}**__",
                                        f"{requested} {interaction.user}",
                                        interaction.user.display_avatar))

    @__set.subcommand(name="welcome_channel", description="Setting server's welcome channel to send welcome messages")
    async def welcome_channel_set(self, interaction: Interaction, channel: Optional[str] = SlashOption(required=True)):
        """
        Parameters
        ----------
        interaction: Interaction
            The interaction object
        channel: str
            Channel to
        """
        channel = int(channel[2:-1])
        channel = (nextcord.utils.get(interaction.guild.text_channels, id=channel))
        if isinstance(channel, nextcord.TextChannel):
            set_welcome_channel(interaction.guild.id, channel.id)
            message = get_msg_from_locale_by_key(interaction.guild.id, f"set_{interaction.application_command.name}")
            requested = get_msg_from_locale_by_key(interaction.guild.id, 'requested_by')
            await interaction.response.send_message(
                embed=construct_basic_embed(interaction.application_command.name,
                                            f"{message} __**{channel}**__",
                                            f"{requested} {interaction.user}",
                                            interaction.user.display_avatar))
        else:
            await interaction.response.send_message('error')

    @__set.subcommand(name="welcome_embed", description="Setting server's welcoming message embed")
    async def welcome_embed_set(self, interaction: Interaction):
        modal = EmbedModal()
        await interaction.response.send_modal(modal)

    @__set.subcommand(name='welcome_message_type', description="Choose bot's welcome message type on your server!")
    async def __welcome_message_type_set(self, interaction: Interaction, welcome_message_type: str = SlashOption(
        name="picker",
        choices={"Welcome message type: photo card": "card",
                 "Welcome message type: embed message": "embed"},
        required=True
    )):
        """
        Parameters
        ----------
        interaction: Interaction
            The interaction object
        welcome_message_type: Optional[str]
            Avialable types of welcome message are card and embed
        """
        update_welcome_message_type(interaction.guild.id, welcome_message_type)
        message = get_msg_from_locale_by_key(interaction.guild.id, f"set_{interaction.application_command.name}")
        requested = get_msg_from_locale_by_key(interaction.guild.id, 'requested_by')
        await interaction.response.send_message(
            embed=construct_basic_embed(interaction.application_command.name,
                                        f"{message} **{welcome_message_type}**",
                                        f"{requested} {interaction.user}",
                                        interaction.user.display_avatar))


def setup(client):
    client.add_cog(Setters(client))
