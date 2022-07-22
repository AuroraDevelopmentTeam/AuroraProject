from typing import Optional

import nextcord
from nextcord import Interaction, Permissions, SlashOption
from nextcord.ext import commands

from core.emotions.create import create_emotion_embed
from core.emotions.storage import kiss_gifs, hug_gifs, idk_gifs, respect_gifs, punch_gifs, cry_gifs, bite_gifs, \
    spank_gifs, five_gifs, pat_gifs, lick_gifs


class Emotions(commands.Cog):
    def __init__(self, client):
        self.client = client

    @nextcord.slash_command(name="emotion", description="Emotions slash command prefix",
                            default_member_permissions=Permissions(moderate_members=True))
    async def __emotion(self, interaction: Interaction):
        """
        This is the emotion slash command that will be the prefix of all emotions commands below.
        """
        pass

    @__emotion.subcommand(name="kiss", description="Emotion command, send kissing emotion mentioning @User")
    async def __kiss(self, interaction: Interaction, user: Optional[nextcord.Member] = SlashOption(required=True),
                     message: Optional[str] = SlashOption(required=False)):
        if user == interaction.user:
            return await interaction.response.send_message('self choose error')
        embed = create_emotion_embed(interaction.guild.id, interaction.application_command.name,
                                     'positive', interaction.user, kiss_gifs, user, message)
        await interaction.response.send_message(embed=embed)

    @__emotion.subcommand(name="hug", description="Emotion command, send hugging emotion mentioning @User")
    async def __hug(self, interaction: Interaction, user: Optional[nextcord.Member] = SlashOption(required=True),
                    message: Optional[str] = SlashOption(required=False)):
        if user == interaction.user:
            return await interaction.response.send_message('self choose error')
        embed = create_emotion_embed(interaction.guild.id, interaction.application_command.name,
                                     'positive', interaction.user, hug_gifs, user, message)
        await interaction.response.send_message(embed=embed)

    @__emotion.subcommand(name="idk", description="Emotion command, send i dont know emotion for author")
    async def __idk(self, interaction: Interaction, message: Optional[str] = SlashOption(required=False)):
        embed = create_emotion_embed(interaction.guild.id, interaction.application_command.name,
                                     'neutral', interaction.user, idk_gifs, author_msg=message)
        await interaction.response.send_message(embed=embed)

    @__emotion.subcommand(name="f", description="PRESS F TO PAY RESPECTS")
    async def __pay_respects(self, interaction: Interaction, message: Optional[str] = SlashOption(required=False)):
        embed = create_emotion_embed(interaction.guild.id, interaction.application_command.name,
                                     'neutral', interaction.user, respect_gifs, author_msg=message)
        await interaction.response.send_message(embed=embed)

    @__emotion.subcommand(name="punch", description="Emotion command, send punching emotion mentioning @User")
    async def __punch(self, interaction: Interaction, user: Optional[nextcord.Member] = SlashOption(required=True),
                      message: Optional[str] = SlashOption(required=False)):
        if user == interaction.user:
            return await interaction.response.send_message('self choose error')
        embed = create_emotion_embed(interaction.guild.id, interaction.application_command.name,
                                     'angry', interaction.user, punch_gifs, user, message)
        await interaction.response.send_message(embed=embed)

    @__emotion.subcommand(name="cry", description="Emotion command, send crying emotion for author")
    async def __cry(self, interaction: Interaction, message: Optional[str] = SlashOption(required=False)):
        embed = create_emotion_embed(interaction.guild.id, interaction.application_command.name,
                                     'sad', interaction.user, cry_gifs, author_msg=message)
        await interaction.response.send_message(embed=embed)

    @__emotion.subcommand(name="bite", description="Emotion command, send bite emotion mentioning @User")
    async def __bite(self, interaction: Interaction, user: Optional[nextcord.Member] = SlashOption(required=True),
                     message: Optional[str] = SlashOption(required=False)):
        if user == interaction.user:
            return await interaction.response.send_message('self choose error')
        embed = create_emotion_embed(interaction.guild.id, interaction.application_command.name,
                                     'blush', interaction.user, bite_gifs, user, message)
        await interaction.response.send_message(embed=embed)

    @__emotion.subcommand(name="spank", description="Emotion command, send spank emotion mentioning @User")
    async def __spank(self, interaction: Interaction, user: Optional[nextcord.Member] = SlashOption(required=True),
                      message: Optional[str] = SlashOption(required=False)):
        if user == interaction.user:
            return await interaction.response.send_message('self choose error')
        embed = create_emotion_embed(interaction.guild.id, interaction.application_command.name,
                                     'blush', interaction.user, spank_gifs, user, message)
        await interaction.response.send_message(embed=embed)

    @__emotion.subcommand(name="highfive", description="Emotion command, send highfive emotion mentioning @User")
    async def __highfive(self, interaction: Interaction, user: Optional[nextcord.Member] = SlashOption(required=True),
                         message: Optional[str] = SlashOption(required=False)):
        if user == interaction.user:
            return await interaction.response.send_message('self choose error')
        embed = create_emotion_embed(interaction.guild.id, interaction.application_command.name,
                                     'friends', interaction.user, five_gifs, user, message)
        await interaction.response.send_message(embed=embed)

    @__emotion.subcommand(name="pat", description="Emotion command, send patting emotion mentioning @User")
    async def __pat(self, interaction: Interaction, user: Optional[nextcord.Member] = SlashOption(required=True),
                    message: Optional[str] = SlashOption(required=False)):
        if user == interaction.user:
            return await interaction.response.send_message('self choose error')
        embed = create_emotion_embed(interaction.guild.id, interaction.application_command.name,
                                     'positive', interaction.user, pat_gifs, user, message)
        await interaction.response.send_message(embed=embed)

    @__emotion.subcommand(name="lick", description="Emotion command, send lick emotion mentioning @User")
    async def __lick(self, interaction: Interaction, user: Optional[nextcord.Member] = SlashOption(required=True),
                     message: Optional[str] = SlashOption(required=False)):
        if user == interaction.user:
            return await interaction.response.send_message('self choose error')
        embed = create_emotion_embed(interaction.guild.id, interaction.application_command.name,
                                     'blush', interaction.user, lick_gifs, user, message)
        await interaction.response.send_message(embed=embed)


def setup(client):
    client.add_cog(Emotions(client))
