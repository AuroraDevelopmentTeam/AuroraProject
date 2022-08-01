from typing import Optional
from easy_pil import *
from PIL import Image
from io import BytesIO
import textwrap

import nextcord
from nextcord.ext import commands, application_checks
from nextcord import Permissions, Interaction, SlashOption

from core.profiles.updaters import update_profile_description, update_avatar_form
from core.money.getters import get_user_balance
from core.honor.getters import get_user_honor_level, get_rome_symbol
from core.levels.getters import get_user_level
from core.profiles.getters import get_profile_description


def get_description_rows(description: str):
    description = description.split(' ')
    return_description = ''
    counter = 1
    for i in description:
        return_description += i
        counter += 1
        if counter % 5 == 0:
            return_description += '\n'
    return rows


class UserProfiles(commands.Cog):
    def __init__(self, client):
        self.client = client

    @nextcord.slash_command(name="profile", default_member_permissions=Permissions(send_messages=True))
    async def __profile(self, interaction: Interaction):
        """
        This is the set slash command that will be the prefix of profile commands.
        """
        pass

    @__profile.subcommand(name="description")
    async def __description_profile(self, interaction: Interaction,
                                    description: Optional[str] = SlashOption(required=True)):
        if len(description) > 140:
            return await interaction.response.send_message('too long error')
        update_profile_description(interaction.user.id, description)
        await interaction.response.send_message('done')

    @__profile.subcommand(name="avatar_form", description="set avatar form for your card commands")
    async def __avatar_form_profile(self, interaction: Interaction, form: str = SlashOption(
        name="picker",
        choices={"circle": "circle", "rounded rectangle": "rectangle"},
        required=True)):
        """
        Parameters
        ----------
        interaction: Interaction
            The interaction object
        form: Optional[str]
            Form of profile avatar
        """
        update_avatar_form(interaction.user.id, form)
        await interaction.response.send_message('done')

    @__profile.subcommand(name="me")
    async def __me_profile(self, interaction: Interaction,
                           user: Optional[nextcord.Member] = SlashOption(required=False)):
        await interaction.response.defer()
        if user is None:
            user = interaction.user
        if user.bot:
            return await interaction.response.send_message('bot_user_error')
        background = Editor(f'./assets/profile.png')
        avatar = BytesIO()
        await user.display_avatar.with_format("png").save(avatar)
        profile_picture = Image.open(avatar)
        profile = Editor(profile_picture).resize((275, 275)).circle_image()
        background.paste(profile, (13, 145))
        level_font = Font.montserrat(size=40)
        larger_font = Font.montserrat(size=40)
        font = Font.montserrat(size=21)
        level = get_user_level(interaction.guild.id, user.id)
        if len(str(level)) == 2:
            coordinates = (715, 70)
        elif len(str(level)) >= 3:
            level_font = Font.montserrat(size=35)
            level = '100+'
            coordinates = (705, 70)
        else:
            coordinates = (725, 70)
        background.text((705, 30), f'LVL', font=larger_font, color="#000000")
        background.text(coordinates, f'{level}', font=level_font, color="#000000")
        background.text((460, 520), str(user.name), font=larger_font, color="#000000")
        honor_level = get_rome_symbol(get_user_honor_level(user.id))
        if len(honor_level) >= 3:
            coordinates = (18, 80)
        elif len(honor_level) == 2:
            if honor_level == "II":
                coordinates = (25, 80)
            elif honor_level == "IV":
                coordinates = (17, 80)
        else:
            if honor_level == "V":
                coordinates = (23, 80)
            elif honor_level == "I":
                coordinates = (30, 80)
        background.text(coordinates, honor_level, font=larger_font, color="#FFFFFF")
        balance = get_user_balance(interaction.guild.id, user.id)
        if balance > 1000000:
            balance = f'{(balance / 1000000):10.2f}KK'
            coordinates = (90, 20)
        elif balance > 10000:
            balance = f'{(balance / 10000):10.2f}K'
            coordinates = (90, 20)
        else:
            coordinates = (130, 20)
        background.text(coordinates, f'{balance}', font=larger_font, color="#FFFFFF")
        description = get_profile_description(user.id)
        lines = textwrap.wrap(description, width=35)
        y_text = 380
        for line in lines:
            width, height = font.getsize(line)
            background.text(((1160 - width) / 2, y_text), line, font=font, color="#FFFFFF")
            y_text += height
        file = nextcord.File(fp=background.image_bytes, filename="profile_card.png")
        await interaction.followup.send(file=file)


def setup(client):
    client.add_cog(UserProfiles(client))
