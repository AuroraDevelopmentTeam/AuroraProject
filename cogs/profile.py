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
from core.badges.getters import get_user_badge_state
from core.badges.converters import ACHIEVMENTS_DESCRIPTION, ACHIEVMENTS_LIST
from core.embeds import DEFAULT_BOT_COLOR
from core.badges.check import check_badges
from core.errors import construct_error_bot_user_embed


def get_description_rows(description: str):
    description = description.split(" ")
    return_description = ""
    counter = 1
    for i in description:
        return_description += i
        counter += 1
        if counter % 5 == 0:
            return_description += "\n"
    return rows


class UserProfiles(commands.Cog):
    def __init__(self, client):
        self.client = client

    @nextcord.slash_command(
        name="profile", default_member_permissions=Permissions(send_messages=True)
    )
    async def __profile(self, interaction: Interaction):
        """
        This is the set slash command that will be the prefix of profile commands.
        """
        pass

    @__profile.subcommand(name="description")
    async def __description_profile(
            self,
            interaction: Interaction,
            description: Optional[str] = SlashOption(required=True),
    ):
        if len(description) > 140:
            embed = nextcord.Embed(
                title="error",
                description=get_msg_from_locale_by_key(
                    interaction.guild.id, "too_long"
                ),
                color=DEFAULT_BOT_COLOR
            )
            return await interaction.response.send_message(embed=embed)
        update_profile_description(interaction.user.id, description)
        message = get_msg_from_locale_by_key(
            interaction.guild.id, f"{interaction.application_command.name}"
        )
        requested = get_msg_from_locale_by_key(interaction.guild.id, "requested_by")
        await interaction.response.send_message(
            embed=construct_basic_embed(
                interaction.application_command.name,
                f"{message} **{description}**",
                f"{requested} {interaction.user}",
                interaction.user.display_avatar,
            )
        )

    @__profile.subcommand(
        name="avatar_form", description="set avatar form for your card commands"
    )
    async def __avatar_form_profile(
            self,
            interaction: Interaction,
            form: str = SlashOption(
                name="picker",
                choices={"circle": "circle", "rounded rectangle": "rectangle"},
                required=True,
            ),
    ):
        """
        Parameters
        ----------
        interaction: Interaction
            The interaction object
        form: Optional[str]
            Form of profile avatar
        """
        update_avatar_form(interaction.user.id, form)
        await interaction.response.send_message("feature in dev")

    @__profile.subcommand(name="me")
    async def __me_profile(
            self,
            interaction: Interaction,
            user: Optional[nextcord.Member] = SlashOption(required=False),
    ):
        await interaction.response.defer()
        check_badges(interaction.guild.id, interaction.user)
        if user is None:
            user = interaction.user
        if user.bot:
            return await interaction.response.send_message(
                embed=construct_error_bot_user_embed(
                    get_msg_from_locale_by_key(interaction.guild.id, "bot_user_error"),
                    self.client.user.avatar.url,
                )
            )
        background = Editor(f"./assets/without_badges.png")
        avatar = BytesIO()
        await user.display_avatar.with_format("png").save(avatar)
        profile_picture = Image.open(avatar)
        profile = Editor(profile_picture).resize((275, 275)).circle_image()
        background.paste(profile, (13, 145))
        level_font = Font.montserrat(size=40)
        larger_font = Font.montserrat(size=40)
        font = Font.montserrat(size=21)
        level = get_user_level(interaction.guild.id, user.id)
        if get_user_badge_state(interaction.guild.id, user.id, "badge_1") is True:
            developer = Editor("./assets/developer_badge.png").resize((35, 35))
            background.paste(developer, (105, 455))
        if get_user_badge_state(interaction.guild.id, user.id, "badge_2") is True:
            developer = Editor("./assets/staff_badge.png").resize((35, 35))
            background.paste(developer, (175, 455))
        if get_user_badge_state(interaction.guild.id, user.id, "badge_3") is True:
            developer = Editor("./assets/golden_wings.png").resize((50, 35))
            background.paste(developer, (245, 455))
        if get_user_badge_state(interaction.guild.id, user.id, "badge_4") is True:
            developer = Editor("./assets/diamond.png").resize((45, 45))
            background.paste(developer, (100, 495))
        if get_user_badge_state(interaction.guild.id, user.id, "badge_5") is True:
            developer = Editor("./assets/honor.png").resize((55, 45))
            background.paste(developer, (165, 495))
        if get_user_badge_state(interaction.guild.id, user.id, "badge_6") is True:
            developer = Editor("./assets/lab.png").resize((35, 35))
            background.paste(developer, (250, 495))
        if get_user_badge_state(interaction.guild.id, user.id, "badge_7") is True:
            developer = Editor("./assets/bug_hunter.png").resize((35, 35))
            background.paste(developer, (105, 545))
        if get_user_badge_state(interaction.guild.id, user.id, "badge_8") is True:
            developer = Editor("./assets/immortal.jpg").resize((45, 45))
            background.paste(developer, (170, 535))
        if get_user_badge_state(interaction.guild.id, user.id, "badge_8") is True:
            developer = Editor("./assets/badge_heart.png").resize((50, 45))
            background.paste(developer, (245, 535))

        if len(str(level)) == 2:
            coordinates = (715, 70)
        elif len(str(level)) >= 3:
            level_font = Font.montserrat(size=35)
            level = "100+"
            coordinates = (705, 70)
        else:
            coordinates = (725, 70)
        background.text((705, 30), f"LVL", font=larger_font, color="#000000")
        background.text(coordinates, f"{level}", font=level_font, color="#000000")
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
            balance = f"{(balance / 1000000):10.2f}KK"
            coordinates = (90, 20)
        elif balance > 10000:
            balance = f"{(balance / 1000):10.2f}K"
            coordinates = (90, 20)
        else:
            coordinates = (130, 20)
        background.text(coordinates, f"{balance}", font=larger_font, color="#FFFFFF")
        description = get_profile_description(user.id)
        lines = textwrap.wrap(description, width=35)
        y_text = 380
        for line in lines:
            width, height = font.getsize(line)
            background.text(
                ((1160 - width) / 2, y_text), line, font=font, color="#FFFFFF"
            )
            y_text += height
        file = nextcord.File(fp=background.image_bytes, filename="profile_card.png")
        await interaction.followup.send(file=file)

    @__profile.subcommand(name="badges", description="show your badges achievements status")
    async def __badges_profile(self,
                               interaction: Interaction):
        embed = nextcord.Embed(color=DEFAULT_BOT_COLOR)
        check_badges(interaction.guild.id, interaction.user)
        for i in range(9):
            state = get_user_badge_state(interaction.guild.id,
                                         interaction.user.id,
                                         f"badge_{i + 1}")
            if state is False:
                state = '**Значок не получен**'
            if state is True:
                state = '**Значок получен**'
            embed.add_field(name=ACHIEVMENTS_LIST[f"badge_{i + 1}"],
                            value=ACHIEVMENTS_DESCRIPTION[f"badge_{i + 1}"] + "\n" + state)
        await interaction.response.send_message(embed=embed)


def setup(client):
    client.add_cog(UserProfiles(client))
