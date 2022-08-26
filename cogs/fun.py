from typing import Optional
import aiohttp

import nextcord
from nextcord.ext import commands
from nextcord import Permissions, Interaction, SlashOption

from core.locales.getters import (
    get_localized_name,
    get_localized_description,
    get_msg_from_locale_by_key,
    get_guild_locale
)
from core.games.brick_knife_evidence_yandere_tentacles import (
    create_starting_embed,
    create_starting_view,
)
from core.fun.ball.storage import get_eight_ball_answer
from core.fun.coin import get_coin_toss
from core.fun.random_api import build_random_image_embed
from core.embeds import construct_basic_embed, DEFAULT_BOT_COLOR


class Funny(commands.Cog):
    def __init__(self, client):
        self.client = client

    @nextcord.slash_command(
        name="brick_knife_evidence_yandere",
        description="Brick Knife Evidence Yandere Tentacles Game",
        name_localizations=get_localized_name("bkeyt"),
        description_localizations=get_localized_description("bkeyt"),
        default_member_permissions=Permissions(send_messages=True),
    )
    async def __brick_knife_evidence_yandere_tentacles(self, interaction: Interaction):
        await interaction.response.defer()
        embed = create_starting_embed(
            get_msg_from_locale_by_key(interaction.guild.id, "bkeyt"),
            get_msg_from_locale_by_key(interaction.guild.id, "pick_one_of_options")
        )
        view = create_starting_view(get_guild_locale(interaction.guild.id))
        await interaction.followup.send(embed=embed, view=view)

    @nextcord.slash_command(name="ball",
                            name_localizations=get_localized_name("ball"),
                            description_localizations=get_localized_description("ball"),
                            default_member_permissions=Permissions(send_messages=True))
    async def __ball(self, interaction: Interaction,
                     question: Optional[str] = SlashOption(required=True,
                                                           description="Question to "
                                                                       "ball",
                                                           name_localizations={
                                                               "ru": "вопрос"},
                                                           description_localizations={
                                                               "ru": "Вопрос шару"
                                                           },
                                                           )):
        await interaction.response.send_message(
            embed=construct_basic_embed(
                interaction.application_command.name,
                get_eight_ball_answer(get_guild_locale(interaction.guild.id)),
                question,
                interaction.user.display_avatar,
                interaction.guild.id
            )
        )

    @nextcord.slash_command(name="coin", description="toss a coin",
                            name_localizations=get_localized_name("coin"),
                            description_localizations=get_localized_description("coin"),
                            default_member_permissions=Permissions(send_messages=True)
                            )
    async def __coin(self, interaction: Interaction):
        image, coin_toss = get_coin_toss(get_guild_locale(interaction.guild.id))
        requested = get_msg_from_locale_by_key(interaction.guild.id, "requested_by")
        embed = construct_basic_embed(
            interaction.application_command.name,
            coin_toss,
            f"{requested} {interaction.user}",
            interaction.user.display_avatar,
            interaction.guild.id
        )
        embed.set_image(url="attachment://coin.png")
        await interaction.response.send_message(
            embed=embed, file=image
        )

    @nextcord.slash_command(name="cat", description="Send's random picture of cat",
                            name_localizations=get_localized_name("cat"),
                            description_localizations=get_localized_description("cat"),
                            default_member_permissions=Permissions(send_messages=True)
                            )
    async def __cat(self, interaction: Interaction):
        async with aiohttp.ClientSession() as session:
            request = await session.get('https://some-random-api.ml/img/cat')
            data = await request.json()
            await interaction.response.send_message(embed=build_random_image_embed(interaction.application_command.name,
                                                                                   data['link'],
                                                                                   interaction.guild.id))

    @nextcord.slash_command(name="dog", description="Send's random picture of dog",
                            name_localizations=get_localized_name("dog"),
                            description_localizations=get_localized_description("dog"),
                            default_member_permissions=Permissions(send_messages=True)
                            )
    async def __dog(self, interaction: Interaction):
        async with aiohttp.ClientSession() as session:
            request = await session.get('https://some-random-api.ml/img/dog')
            data = await request.json()
            await interaction.response.send_message(embed=build_random_image_embed(interaction.application_command.name,
                                                                                   data['link'],
                                                                                   interaction.guild.id))

    @nextcord.slash_command(name="fox", description="Send's random picture of fox",
                            name_localizations=get_localized_name("fox"),
                            description_localizations=get_localized_description("fox"),
                            default_member_permissions=Permissions(send_messages=True)
                            )
    async def __fox(self, interaction: Interaction):
        async with aiohttp.ClientSession() as session:
            request = await session.get('https://some-random-api.ml/img/fox')
            data = await request.json()
            await interaction.response.send_message(embed=build_random_image_embed(interaction.application_command.name,
                                                                                   data['link'],
                                                                                   interaction.guild.id))

    @nextcord.slash_command(name="bird", description="Send's random picture of bird",
                            name_localizations=get_localized_name("bird"),
                            description_localizations=get_localized_description("bird"),
                            default_member_permissions=Permissions(send_messages=True)
                            )
    async def __birb(self, interaction: Interaction):
        async with aiohttp.ClientSession() as session:
            request = await session.get('https://some-random-api.ml/img/birb')
            data = await request.json()
            await interaction.response.send_message(embed=build_random_image_embed(interaction.application_command.name,
                                                                                   data['link'],
                                                                                   interaction.guild.id))

    @nextcord.slash_command(name="panda", description="Send's random picture of panda",
                            name_localizations=get_localized_name("panda"),
                            description_localizations=get_localized_description("panda"),
                            default_member_permissions=Permissions(send_messages=True)
                            )
    async def __panda(self, interaction: Interaction):
        async with aiohttp.ClientSession() as session:
            request = await session.get('https://some-random-api.ml/img/panda')
            data = await request.json()
            await interaction.response.send_message(embed=build_random_image_embed(interaction.application_command.name,
                                                                                   data['link'],
                                                                                   interaction.guild.id))

    @nextcord.slash_command(name="red_panda", description="Send's random picture of red panda",
                            name_localizations=get_localized_name("red_panda"),
                            description_localizations=get_localized_description("red_panda"),
                            default_member_permissions=Permissions(send_messages=True)
                            )
    async def __red_panda(self, interaction: Interaction):
        async with aiohttp.ClientSession() as session:
            request = await session.get('https://some-random-api.ml/img/red_panda')
            data = await request.json()
            await interaction.response.send_message(embed=build_random_image_embed(interaction.application_command.name,
                                                                                   data['link'],
                                                                                   interaction.guild.id))


def setup(client):
    client.add_cog(Funny(client))
