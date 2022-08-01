import nextcord
from nextcord.ext import commands, application_checks
from nextcord import Interaction, Permissions
from core.embeds import construct_top_embed
from core.money.getters import get_guild_currency_symbol
from core.locales.getters import get_msg_from_locale_by_key


class TicketSettings(nextcord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @nextcord.ui.button(
        label="Close ticket", style=nextcord.ButtonStyle.red, custom_id="ticket_settings:red"
    )
    async def close_ticket(self, button: nextcord.ui.Button, interaction: Interaction):
        pass


class CreateTicket(nextcord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @nextcord.ui.button(
        label="Create ticket", style=nextcord.ButtonStyle.blurple, custom_id="create_ticket:blurple"
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
            custom_id = (interaction.data['custom_id'])
            if custom_id == 'create_ticket:blurple':
                embed = nextcord.Embed(title="Ticket", description=f"Your ticket is creating...")
                msg = await interaction.response.send_message(embed=embed, ephemeral=True)
                overwrites = {
                    interaction.guild.default_role: nextcord.PermissionOverwrite(read_messages=False),
                    interaction.guild.me: nextcord.PermissionOverwrite(read_messages=True),
                }
                channel = await interaction.guild.create_text_channel(f"{interaction.user.name}-ticket",
                                                                      overwrites=overwrites)
                embed = nextcord.Embed(title="Ticket",
                                       description=f"Your ticket created! Click here: {channel.mention}")
                await msg.edit(embed=embed)
                embed = nextcord.Embed(title="Ticket", description=f"{interaction.user.mention} created a ticket!")
                await channel.send(embed=embed, view=TicketSettings())
            if custom_id == 'ticket_settings:red':
                await interaction.channel.send('Closing this ticket...')
                await interaction.channel.delete()
                await interaction.user.send(f'Ticket closed!')
        except KeyError:
            pass

    @nextcord.slash_command(name="setup_tickets", default_member_permissions=Permissions(administrator=True))
    @application_checks.has_permissions(manage_guild=True)
    async def __ticket(self, interaction: Interaction):
        embed = nextcord.Embed(title="Create a ticket",
                               description="Click `create ticket` button below to create a ticket. "
                                           "The server's staff will be notified and solve your problem.")
        await interaction.response.send_message(embed=embed, view=CreateTicket())


def setup(client):
    client.add_cog(Tickets(client))