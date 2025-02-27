from typing import Optional
import psutil
import locale

import nextcord
from nextcord import Interaction, SlashOption, Permissions
from nextcord.ext import commands

from core.locales.getters import (
    get_msg_from_locale_by_key,
    get_keys_value_in_locale,
    get_localized_description,
    get_localized_name,
    get_guild_locale,
)
from core.embeds import construct_basic_embed, construct_long_embed, DEFAULT_BOT_COLOR
from core import EmbedCreator


class Information(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.cooldown(1, 50, commands.BucketType.guild)
    @nextcord.slash_command(
        name="ping",
        description="Shows client's ping",
        name_localizations=get_localized_name("ping"),
        description_localizations=get_localized_description("ping"),
        default_member_permissions=Permissions(send_messages=True),
    )
    # @cooldowns.cooldown(1, 15, bucket=cooldowns.SlashBucket.author)
    async def __ping(self, interaction: Interaction):
        message = get_msg_from_locale_by_key(
            interaction.guild.id, interaction.application_command.name
        )
        requested = get_msg_from_locale_by_key(interaction.guild.id, "requested_by")

        await interaction.response.send_message(
            embed=construct_basic_embed(
                interaction.application_command.name,
                f"{message} {round(self.client.get_shard(interaction.guild.shard_id).latency * 1000)} ms",
                f"{requested} {interaction.user}",
                interaction.user.display_avatar,
                interaction.guild.id,
            )
        )

    @nextcord.slash_command(
        name="server",
        description="Sends all information about server, that can i found",
        name_localizations=get_localized_name("server"),
        description_localizations=get_localized_description("server"),
        default_member_permissions=Permissions(send_messages=True),
    )
    async def __server(self, interaction: Interaction):
        guild = interaction.guild
        requested = get_msg_from_locale_by_key(interaction.guild.id, "requested_by")
        names_of_embed_fields = get_keys_value_in_locale(
            guild.id, interaction.application_command.name
        )
        if get_guild_locale(interaction.guild.id) == "ru_ru":
            locale.setlocale(locale.LC_ALL, "ru_RU.UTF-8")
        else:
            locale.setlocale(locale.LC_ALL, "en_US.UTF-8")
        if guild.icon is None:  # Фикс команды при отсутствии у сервера иконки
            embedicon = "https://ui-avatars.com/api/?name=" + f"{guild.name}".replace(
                " ", "+"
            )
        else:
            embedicon = guild.icon
        guild = await self.client.fetch_guild(interaction.guild.id)
        users = guild.approximate_member_count
        embed = construct_long_embed(
            f"{guild.name}:",
            embedicon,  # Тут был guild.icon (помним любим скорбим)
            f"{requested} {interaction.user}",
            interaction.user.display_avatar,
            names_of_embed_fields,
            [
                f"```\n{users} 🧍\n```",
                f"```{await self.client.fetch_user(guild.owner_id)}```",
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
            ],
            True,
        )
        await interaction.response.send_message(embed=embed)

    @nextcord.slash_command(
        name="user",
        description="Sends all information about user, that can i found",
        name_localizations=get_localized_name("user"),
        description_localizations=get_localized_description("user"),
        default_member_permissions=Permissions(send_messages=True),
    )
    async def __user(
            self,
            interaction: Interaction,
            user: Optional[nextcord.Member] = SlashOption(
                required=True,
                description="The discord's user, tag someone with @",
                description_localizations={
                    "ru": "Пользователь дискорда, укажите кого-то @"
                },
            ),
    ):
        if user is None:
            return await interaction.response.send_message("no key value error 786")
        requested = get_msg_from_locale_by_key(interaction.guild.id, "requested_by")
        names_of_embed_fields = get_keys_value_in_locale(
            interaction.guild.id, interaction.application_command.name
        )
        try:
            activity = user.activity.name
        except AttributeError:
            activity = user.activity
        embed = construct_long_embed(
            f"{user.name}:",
            user.avatar,
            f"{requested} {interaction.user}",
            interaction.user.display_avatar,
            names_of_embed_fields,
            [
                f"{nextcord.utils.format_dt(user.created_at)}",
                f"#{user.discriminator}",
                f"{nextcord.utils.format_dt(user.joined_at)}",
                f"```{user.desktop_status}```",
                f"```{user.web_status}```",
                f"```{user.mobile_status}```",
                f"```{user.id}```",
                f"```{user.nick}```",
                f"```{len(user.roles)}```",
                f"{activity}",
            ],
            True,
        )
        await interaction.response.send_message(embed=embed)

    @nextcord.slash_command(name="about_aurora",
                            description="Sends all information about Aurora bot",
                            name_localizations=get_localized_name("about_aurora"),
                            description_localizations=get_localized_description("about_aurora"),
                            default_member_permissions=Permissions(send_messages=True),
                            )
    async def __about_aurora(self, interaction: Interaction):
        requested = get_msg_from_locale_by_key(interaction.guild.id, "requested_by")
        names_of_embed_fields = get_keys_value_in_locale(
            interaction.guild.id, interaction.application_command.name
        )
        embed = construct_long_embed(
            f"{self.client.user}:",
            self.client.user.avatar.url,
            f"{requested} {interaction.user}",
            interaction.user.display_avatar,
            names_of_embed_fields,
            [
                f"```\n{len(self.client.users)} 🧍```",
                f"```{len(self.client.guilds)}```",
                f"```{self.client.user.id}```",
                f"```{psutil.cpu_percent()}```",
                f"```{psutil.virtual_memory().percent}```",
                f"```{round((psutil.virtual_memory().available * 100 / psutil.virtual_memory().total), 1)}```",
                f"```{interaction.guild.shard_id}```",
                f"```{self.client.status}```",
                f"{nextcord.utils.format_dt(self.client.user.created_at)}",
                f"```Python 3.10.4```",
                f"```Nextcord```",
                f"[GitHub](https://github.com/AuroraDevelopmentTeam)",
            ],
            True,
        )
        await interaction.response.send_message(embed=embed)

    @nextcord.slash_command(name='test', guild_ids=[795308018593562624])
    async def embed2(self, interaction: Interaction):
        """Embed Generator With Default Embed And Author Check So Only The Invoker Can Use The Editor"""
        view = EmbedCreator(bot=self.client)
        author = interaction.user

        async def check(interaction: nextcord.Interaction):
            if interaction.user.id == author.id:
                return True
            await interaction.response.send_message(f"Only {author} can use this interaction!", ephemeral=True)
            return False

        view.interaction_check = check
        await interaction.response.send_message(embed=view.get_default_embed, view=view)


def setup(client):
    client.add_cog(Information(client))
