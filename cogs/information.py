import nextcord
from nextcord import Interaction, SlashOption, Permissions
from nextcord.ext import commands
from core.locales.getters import get_msg_from_locale_by_key, get_keys_value_in_locale, get_localized_description, \
    get_localized_name
from core.embeds import construct_basic_embed, construct_long_embed, DEFAULT_BOT_COLOR
from typing import Optional
import cooldowns


class Information(commands.Cog):

    def __init__(self, client):
        self.client = client

    @nextcord.slash_command(name="help", description="Shows help menu",
                            default_member_permissions=Permissions(send_messages=True))
    async def __help(self, interaction: Interaction):
        embed = nextcord.Embed(color=DEFAULT_BOT_COLOR, title=interaction.application_command.name.capitalize())
        embed.add_field(name='Info', value='`help` `ping` `server` `user @`', inline=False)
        embed.add_field(name='Levels', value='`level [@]` `set level <@> <number>` `set level_up_messages <on/off>`', inline=False)
        embed.add_field(name='Moderation', value='`mute <@> <time> [reason]` `unmute <@>` `mutes` `clear <amount>` '
                                                 '`warn <@> [reason]` `unwarn @ <warn_id>` `warns <@>`',
                        inline=False)
        embed.add_field(name='Economics', value='`add_money <@> <$>` `remove_money <@> <$>` `money` `reset money <@>` '
                                                '`reset economics` `set currency <symbol>` `set start_balance <$>`'
                                                ' `set timely_amount <$>` `give <@> <$>` `timely` ', inline=False)
        embed.add_field(name='Games', value='`blackjack` `slots` `brick_knife_evidence_yandere`', inline=False)
        embed.add_field(name='Locales', value='`set locale <locale>`', inline=False)
        embed.add_field(name='Welcome messages', value='`set welcome_channel <#channel>`'
                                                       ' `set welcome_message_type <card/embed>` `set welcome_embed`'
                                                       ' `welcome_message_state <on/of>`', inline=False)
        await interaction.response.send_message(embed=embed)

    @commands.cooldown(1, 50, commands.BucketType.guild)
    @nextcord.slash_command(name="ping", description="Shows client's ping",
                            name_localizations=get_localized_name("ping"),
                            description_localizations=get_localized_description("ping"),
                            default_member_permissions=Permissions(send_messages=True))
    # @cooldowns.cooldown(1, 15, bucket=cooldowns.SlashBucket.author)
    async def __ping(self, interaction: Interaction):
        message = get_msg_from_locale_by_key(interaction.guild.id, interaction.application_command.name)
        requested = get_msg_from_locale_by_key(interaction.guild.id, 'requested_by')
        await interaction.response.send_message(
            embed=construct_basic_embed(interaction.application_command.name,
                                        f"{message} {round(self.client.latency * 1000)} ms",
                                        f"{requested} {interaction.user}",
                                        interaction.user.display_avatar))

    @nextcord.slash_command(name="server", description="Sends all information about server, that can i found",
                            name_localizations=get_localized_name("server"),
                            description_localizations=get_localized_description("server"),
                            default_member_permissions=Permissions(send_messages=True))
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
                                      ], True)
        await interaction.response.send_message(embed=embed)

    @nextcord.slash_command(name="user", description="Sends all information about user, that can i found",
                            default_member_permissions=Permissions(send_messages=True))
    async def __user(self, interaction: Interaction,
                     user: Optional[nextcord.Member] = SlashOption(required=True, description="The discord's user, "
                                                                                              "tag someone with @",
                                                                   description_localizations={"ru": "Пользователь "
                                                                                                    "дискорда"})):
        if user is None:
            return await interaction.response.send_message('no key value error 786')
        requested = get_msg_from_locale_by_key(interaction.guild.id, 'requested_by')
        names_of_embed_fields = get_keys_value_in_locale(interaction.guild.id, interaction.application_command.name)
        embed = construct_long_embed(f'{user.name}:', user.avatar, f"{requested} {interaction.user}",
                                     interaction.user.display_avatar,
                                     names_of_embed_fields,
                                     [f"```{user.created_at.strftime('%a, %d %b %Y')}```",
                                      f"```#{user.discriminator}```",
                                      f"```{user.joined_at.strftime('%a, %d %b %Y')}```",
                                      f"```{user.desktop_status}```",
                                      f"```{user.web_status}```",
                                      f"```{user.mobile_status}```",
                                      f"```{user.id}```",
                                      f"```{user.nick}```",
                                      f"```{len(user.roles)}```",
                                      f"{user.activity}"
                                      ], True)
        await interaction.response.send_message(embed=embed)


def setup(client):
    client.add_cog(Information(client))
