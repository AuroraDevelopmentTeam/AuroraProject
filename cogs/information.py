import nextcord
from nextcord import Interaction
from nextcord.ext import commands
from config import settings
from core.locales import get_msg_from_locale_by_key, get_keys_of_command_in_locale, get_keys_value_in_locale
from core.embeds import construct_basic_embed, construct_long_embed


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

    @nextcord.slash_command(name="server", description="Sends all information about server, that can i found")
    async def __server(self, interaction: Interaction):
        guild = interaction.guild
        requested = get_msg_from_locale_by_key(interaction.guild.id, 'requested_by')
        names_of_embed_fields = get_keys_value_in_locale(guild.id, interaction.application_command.name)
        embed = construct_long_embed(f'{guild.name}:', guild.icon, f"{requested} {interaction.user}",
                                     interaction.user.display_avatar,
                                     names_of_embed_fields,
                                     [f"```\n{guild.member_count}\n{len(guild.humans)} 🧍 {len(guild.bots)} 🤖\n```",
                                      f"```{guild.owner.name}```",
                                      f"```{len(guild.emojis)}```",
                                      f"```{guild.created_at.strftime('%a, %d %b %Y')}```",
                                      f"```{guild.id}```",
                                      f"```{len(guild.channels)}```",
                                      f"```{len(guild.voice_channels)}```",
                                      f"```{len(guild.text_channels)}```",
                                      f"```{len(guild.categories)}```",
                                      f"```{len(guild.roles)}```",
                                      f"```{guild.shard_id}```",
                                      f"```{guild.explicit_content_filter}```",
                                      f"```{guild.description}```",
                                      f"```{guild.premium_tier}```",
                                      f"```{guild.premium_subscription_count}```",
                                      ])
        await interaction.response.send_message(embed=embed)


def setup(client):
    client.add_cog(Information(client))
