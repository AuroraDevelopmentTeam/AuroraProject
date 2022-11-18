import nextcord
from nextcord.ext import commands, application_checks
from nextcord import Interaction, Permissions, SlashOption

from core.embeds import construct_top_embed
from core.money.getters import get_guild_currency_symbol
from core.locales.getters import (
    get_msg_from_locale_by_key,
    get_guild_locale,
    get_localized_name,
    get_localized_description,
)
from core.tickets.getters import (
    get_ticket_archive,
    get_ticket_category,
    get_ticket_support,
)
from core.tickets.updaters import update_ticket_archive, update_ticket_category
from core.embeds import DEFAULT_BOT_COLOR
from core.errors import construct_error_command_is_active


class TicketDisabledEng(nextcord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @nextcord.ui.button(
        label="Close ticket",
        style=nextcord.ButtonStyle.red,
        custom_id="ticket_settings:red",
        disabled=True,
    )
    async def close_ticket(self, button: nextcord.ui.Button, interaction: Interaction):
        pass


class TicketSettingsEng(nextcord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @nextcord.ui.button(
        label="Close ticket",
        style=nextcord.ButtonStyle.red,
        custom_id="ticket_settings:red",
        disabled=False,
    )
    async def close_ticket(self, button: nextcord.ui.Button, interaction: Interaction):
        pass


class CreateTicketEng(nextcord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @nextcord.ui.button(
        label="Create a ticket",
        style=nextcord.ButtonStyle.blurple,
        custom_id="create_ticket:blurple",
    )
    async def create_ticket(self, button: nextcord.ui.Button, interaction: Interaction):
        pass


class TicketDisabledRu(nextcord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @nextcord.ui.button(
        label="Создать Тикет",
        style=nextcord.ButtonStyle.red,
        custom_id="ticket_settings:red",
        disabled=True,
    )
    async def close_ticket(self, button: nextcord.ui.Button, interaction: Interaction):
        pass


class TicketSettingsRu(nextcord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @nextcord.ui.button(
        label="Закрыть Тикет",
        style=nextcord.ButtonStyle.red,
        custom_id="ticket_settings:red",
        disabled=False,
    )
    async def close_ticket(self, button: nextcord.ui.Button, interaction: Interaction):
        pass


class CreateTicketRu(nextcord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @nextcord.ui.button(
        label="Создать Тикет",
        style=nextcord.ButtonStyle.blurple,
        custom_id="create_ticket:blurple",
    )
    async def create_ticket(self, button: nextcord.ui.Button, interaction: Interaction):
        pass


class Tickets(commands.Cog):
    def __init__(self, client):
        self.client = client
        super().__init__()
        self.persistent_views_added = True

    async def on_ready(self):
        if not self.persistent_views_added:
            self.add_view(CreateTicket())
            self.persistent_views_added = True

    @commands.Cog.listener()
    async def on_interaction(self, interaction: Interaction):
        try:
            custom_id = interaction.data["custom_id"]
            if custom_id == "create_ticket:blurple":
                try:
                    await interaction.response.defer()
                except:
                    pass
                if get_ticket_category(interaction.guild.id) == 0:
                    return
                embed = nextcord.Embed(
                    title=get_msg_from_locale_by_key(interaction.guild.id, "ticket"),
                    description=get_msg_from_locale_by_key(
                        interaction.guild.id, "ticket_creating"
                    ),
                    color=DEFAULT_BOT_COLOR,
                )
                msg = await interaction.followup.send(embed=embed, ephemeral=True)
                support_role = nextcord.utils.get(
                    interaction.guild.roles, id=get_ticket_support(interaction.guild.id)
                )
                if support_role is not None:
                    overwrites = {
                        interaction.guild.default_role: nextcord.PermissionOverwrite(
                            read_messages=False
                        ),
                        interaction.user: nextcord.PermissionOverwrite(read_messages=True),
                        support_role: nextcord.PermissionOverwrite(read_messages=True),
                    }
                else:
                    overwrites = {
                        interaction.guild.default_role: nextcord.PermissionOverwrite(
                            read_messages=False
                        ),
                        interaction.user: nextcord.PermissionOverwrite(read_messages=True),
                    }
                tickets_category = get_ticket_category(interaction.guild.id)
                category_channel = nextcord.utils.get(
                    interaction.guild.categories, id=tickets_category
                )
                for channel in category_channel.channels:
                    if str(channel.name.casefold()) == f"{str(interaction.user.name.casefold())}":
                        embed = construct_error_command_is_active(
                            get_msg_from_locale_by_key(
                                interaction.guild.id, "command_is_active_error"
                            ),
                            interaction.user.display_avatar,
                        )
                        return await interaction.followup.send(embed=embed, ephemeral=True)
                channel = await interaction.guild.create_text_channel(name=f"{interaction.user.name}",
                                                                      category=category_channel,
                                                                      overwrites=overwrites)
                embed = nextcord.Embed(
                    title=get_msg_from_locale_by_key(interaction.guild.id, "ticket"),
                    description=f"{get_msg_from_locale_by_key(interaction.guild.id, 'ticket_now_is_created')} "
                                f"{channel.mention}",
                    color=DEFAULT_BOT_COLOR,
                )
                await msg.edit(embed=embed)
                embed = nextcord.Embed(
                    title=get_msg_from_locale_by_key(interaction.guild.id, "ticket"),
                    description=f"{interaction.user.mention} "
                                f"{get_msg_from_locale_by_key(interaction.guild.id, 'created_ticket')}",
                    color=DEFAULT_BOT_COLOR,
                )
                if get_guild_locale(interaction.guild.id) == "ru_ru":
                    await channel.send(embed=embed, view=TicketSettingsRu())
                else:
                    await channel.send(embed=embed, view=TicketSettingsEng())
            if custom_id == "ticket_settings:red":
                if get_ticket_archive(interaction.guild.id) == 0:
                    return
                await interaction.channel.send(
                    get_msg_from_locale_by_key(interaction.guild.id, "ticket_closing")
                )
                archive_channel = get_ticket_archive(interaction.guild.id)
                category_channel = nextcord.utils.get(
                    interaction.guild.categories, id=archive_channel
                )
                overwrites = {
                    interaction.guild.default_role: nextcord.PermissionOverwrite(
                        read_messages=False
                    )
                }
                try:
                    await interaction.user.send(
                        f"{get_msg_from_locale_by_key(interaction.guild.id, 'ticket_closed')}"
                    )
                except nextcord.Forbidden:
                    pass
                if get_guild_locale(interaction.guild.id) == "ru_ru":
                    await interaction.message.edit(view=TicketDisabledRu())
                else:
                    await interaction.message.edit(view=TicketDisabledEng())
                await interaction.channel.send(
                    f"{get_msg_from_locale_by_key(interaction.guild.id, 'ticket_closed')}"
                )
                await interaction.channel.edit(
                    category=category_channel,
                    overwrites=overwrites,
                    sync_permissions=True,
                )
        except KeyError:
            pass

    @application_checks.bot_has_guild_permissions(manage_channels=True)
    @application_checks.has_permissions(manage_guild=True)
    @nextcord.slash_command(
        name="setup_tickets",
        name_localizations=get_localized_name("setup_tickets"),
        description_localizations=get_localized_description("setup_tickets"),
        default_member_permissions=Permissions(administrator=True),
    )
    async def __setup_tickets(
            self,
            interaction: Interaction,
            create_mode: str = SlashOption(
                name="picker", choices={"auto": "auto", "self": "self"}, required=True
            ),
    ):
        await interaction.response.defer()
        embed = nextcord.Embed(
            title=get_msg_from_locale_by_key(interaction.guild.id, "create_ticket"),
            description=get_msg_from_locale_by_key(interaction.guild.id, "ticket_desc"),
            color=DEFAULT_BOT_COLOR,
        )
        if create_mode == "auto":
            overwrites = {
                interaction.guild.default_role: nextcord.PermissionOverwrite(
                    read_messages=False
                ),
                interaction.guild.me: nextcord.PermissionOverwrite(read_messages=True),
            }
            tickets_category = await interaction.guild.create_category(
                name=f"Aurora-Tickets", overwrites=overwrites
            )
            update_ticket_category(interaction.guild.id, tickets_category.id)
            archive_category = await interaction.guild.create_category(
                name="Aurora-Archive", overwrites=overwrites
            )
            update_ticket_archive(interaction.guild.id, archive_category.id)
        if get_guild_locale(interaction.guild.id) == "ru_ru":
            await interaction.followup.send(embed=embed, view=CreateTicketRu())
        else:
            await interaction.followup.send(embed=embed, view=CreateTicketEng())


def setup(client):
    client.add_cog(Tickets(client))
