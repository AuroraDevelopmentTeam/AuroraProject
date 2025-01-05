from __future__ import annotations

import nextcord
from nextcord import Asset
from config import settings
from nextcord.ext import commands
from core.locales.getters import get_msg_from_locale_by_key, localize_name
from core.emojify import CLOCK
from core.utils import MobilePlatform, DesktopPlatform, calculate_platform_type
from core.locales.getters import get_guild_locale

from typing import Callable, Dict
from core.utils import ModalInput, SelectPrompt
from nextcord import Colour, Embed, HTTPException, Interaction, SelectOption, TextInputStyle
from nextcord.ui import TextInput, Modal

DEFAULT_BOT_COLOR = settings["default_color"]


def construct_error_embed(description: str) -> nextcord.Embed:
    embed = nextcord.Embed(color=DEFAULT_BOT_COLOR, description=description)
    return embed


def construct_basic_embed(
        name: str, value: str, footer_text: str, footer_url: Asset, guild_id: int
) -> nextcord.Embed:
    try:
        if name == "timely":
            name = f"{localize_name(guild_id, name).capitalize()}"
            name = CLOCK + " " + name
        else:
            name = localize_name(guild_id, name)
            name = name.capitalize()
    except Exception as error:
        name = name
        name = name.capitalize()
    name = name.replace("_", " ")
    embed = nextcord.Embed(color=DEFAULT_BOT_COLOR)
    embed.add_field(name=name, value=value)
    embed.set_footer(text=footer_text, icon_url=footer_url)
    return embed


def construct_long_embed(
        title: str,
        thumbnail_url: Asset,
        footer_text: str,
        footer_url: Asset,
        name_list: list,
        value_list: list,
        inline: bool,
) -> nextcord.Embed:
    title = title.capitalize()
    embed = nextcord.Embed(color=DEFAULT_BOT_COLOR, title=title)
    embed.set_footer(text=footer_text, icon_url=footer_url)
    embed.set_thumbnail(url=thumbnail_url)
    if len(name_list) == len(value_list):
        for name, value in zip(name_list, value_list):
            embed.add_field(name=name, value=value, inline=inline)
    return embed


def construct_leaderboard_embed(guild_id: int, leaderboard_name: str, value: str, user_list: list[nextcord.Member],
                                values_list: list[str]) -> nextcord.Embed:
    embed = nextcord.Embed(color=DEFAULT_BOT_COLOR, title=leaderboard_name)
    counter = 0
    if get_guild_locale(guild_id) == "ru_ru":
        field_names = ["#.", "Никнейм", value]
    else:
        field_names = ["#.", "Nickname", value]
    for i in range(len(user_list)):
        counter += 1
        embed.add_field(name=field_names[0], value=counter)
        embed.add_field(name=field_names[1], value=user_list[i])
        embed.add_field(name=field_names[2], value=values_list[i])
    return embed


def construct_top_embed(
        title: str,
        top_list: list,
        footer_text: str,
        footer_url: Asset,
        currency_symbol=None,
        guild=None,
) -> nextcord.Embed:
    if guild is not None:
        msg = get_msg_from_locale_by_key(guild.id, "price")
    title = title.capitalize()
    counter = 0
    users = []
    for row in top_list:
        counter += 1
        if currency_symbol is not None:
            if guild is not None:
                msg = get_msg_from_locale_by_key(guild.id, "price")
                users.append(
                    f"**{counter}** • {row[0]}\n> {msg} **{row[1]}** {currency_symbol}\n"
                )
            else:
                users.append(
                    f"**{counter}** • {row[0]}\n> **{row[1]}** {currency_symbol}\n"
                )
        else:
            if len(top_list) > 2:
                counter = row[2]
            else:
                pass
            users.append(f"**{counter}** • {row[0]}\n> {row[1]}\n")
    if len(users) > 0:
        description = " ".join([user for user in users])
    else:
        description = "..."
    embed = nextcord.Embed(
        color=DEFAULT_BOT_COLOR, title=title, description=description
    )
    embed.set_footer(text=footer_text, icon_url=footer_url)
    return embed


def construct_log(
        event_type: str,
        guild: nextcord.Guild,
        message: nextcord.Message = None,
        jump_url: bool = False,
        display_message: bool = True,
        message_channel: nextcord.TextChannel = None,
        user: nextcord.Member = None,
        before: nextcord.Message = None,
        after: nextcord.Message = None,
        role: nextcord.Role = None,
        role_before: nextcord.Role = None,
        role_after: nextcord.Role = None,
        channel=None,
        channel_before=None,
        channel_after=None,
) -> nextcord.Embed:
    embed = nextcord.Embed(color=DEFAULT_BOT_COLOR, title=event_type)
    if message_channel is not None:
        embed.add_field(
            name="Channel",
            value=f"{message_channel.mention}\nID: **{message_channel.id}**",
            inline=False,
        )
    if user is not None:
        embed.add_field(
            name="User",
            value=f"{user.mention}\n`{user}`, ID: **{user.id}**",
            inline=False,
        )
        embed.set_thumbnail(url=f"{user.display_avatar}")
    if jump_url is True:
        embed.add_field(
            name="URL", value=f"[message]({message.jump_url})", inline=False
        )
    if message is not None and display_message is True:
        embed.add_field(name="Message", value=f"``{message.content}``", inline=False)
    if before is not None:
        embed.add_field(name="Before", value=f"``{before.content}``", inline=True)
    if after is not None:
        embed.add_field(name="After", value=f"``{after.content}``", inline=True)
    if role is not None:
        embed.add_field(
            name="Role",
            value=f"{role.mention}\n"
                  f"ID: **{role.id}**, name: ``{role.name}``\n"
                  f"Position: **{role.position}**, mentionable: **{role.mentionable}**\n"
                  f"Permissions: **{role.permissions.value}**",
            inline=False,
        )
    if role_before is not None:
        embed.add_field(
            name="Before",
            value=f"``@{role_before.name}``, ``{role_before.color}``\n"
                  f"Position: **{role_before.position}**, mentionable: "
                  f"**{role_before.mentionable}**\n"
                  f"Permissions: **{role_before.permissions.value}**",
            inline=True,
        )
    if role_after is not None:
        embed.add_field(
            name="After",
            value=f"{role_after.mention}\n``@{role_after.name}``, ``{role_after.color}``\n"
                  f"Position: **{role_after.position}**, mentionable: "
                  f"**{role_after.mentionable}**\n"
                  f"Permissions: **{role_after.permissions.value}**",
            inline=True,
        )
    if channel is not None:
        embed.add_field(
            name="Channel", value=f"``{channel.name}``, {channel.mention}", inline=False
        )
    if channel_before is not None:
        embed.add_field(name="Before", value=f"``{channel_before.name}``", inline=True)
    if channel_after is not None:
        embed.add_field(
            name="After",
            value=f"``{channel_after.name}``, {channel_after.mention}",
            inline=True,
        )
    embed.set_footer(text=f"{guild.name}\nAURORA", icon_url=guild.icon)
    return embed


class CreatorMethods:
    """
    Класс содержит методы для редактирования Embed.
    """

    def __init__(self, embed: Embed) -> None:
        self.embed = embed
        self.callbacks: Dict[str, Callable] = {
            "author": self.edit_author,
            "message": self.edit_message,
            "thumbnail": self.edit_thumbnail,
            "image": self.edit_image,
            "footer": self.edit_footer,
            "color": self.edit_colour,
            "addfield": self.add_field,
            "removefield": self.remove_field,
        }

    async def edit_author(self, interaction: Interaction) -> None:
        """This method edits the embed's author"""
        print("edit_author called")  # отладка
        try:
            modal = ModalInput(title="Edit Embed Author")
            modal.add_item(
                TextInput(
                    label="Author Name",
                    max_length=100,
                    default_value=self.embed.author.name,
                    placeholder="Author name to display in the embed",
                    required=False,
                )
            )
            modal.add_item(
                TextInput(
                    label="Author Icon Url",
                    default_value=self.embed.author.icon_url,
                    placeholder="Author icon to display in the embed",
                    required=False,
                )
            )
            modal.add_item(
                TextInput(
                    label="Author Url",
                    default_value=self.embed.author.url,
                    placeholder="URL to set as the embed's author link",
                    required=False,
                )
            )
            await interaction.response.send_modal(modal)
            print("Modal sent")  # отладка

            # await modal.wait()
            async def callback(interaction):
                print("Modal response received")  # отладка
                name = modal.children[0].value
                icon_url = modal.children[1].value
                url = modal.children[2].value
                print(name, icon_url, url)
                try:
                    self.embed.set_author(
                        name=name,
                        icon_url=icon_url,
                        url=url,
                    )
                except HTTPException as e:
                    print(f"HTTPException: {e}")
                    self.embed.set_author(name=str(modal.children[0]))
                try:
                    await interaction.message.edit(embed=self.embed)
                    print("Embed updated successfully.")
                except Exception as e:
                    print(f"Failed to update embed: {e}")

            modal.callback = callback
        except Exception as e:
            print(f"Error in edit_author: {e}")
            await interaction.response.send_message("There was an error processing your request.", ephemeral=True)

    async def edit_message(self, interaction: Interaction) -> None:
        """Редактирование заголовка и описания эмбеда"""
        try:
            modal = Modal(title="Edit Embed Message")
            modal.add_item(
                TextInput(
                    label="Embed Title",
                    style=TextInputStyle.short,
                    default_value=self.embed.title or "",
                    placeholder="Title to display in the embed",
                    max_length=255,
                    required=False,
                )
            )
            modal.add_item(
                TextInput(
                    label="Embed Description",
                    style=TextInputStyle.paragraph,
                    default_value=self.embed.description or "",
                    placeholder="Description to display in the embed",
                    max_length=2000,
                    required=False,
                )
            )

            await interaction.response.send_modal(modal)
            # await modal.wait()

            async def callback(interaction):

                # Проверка значений, которые были введены
                new_title = modal.children[0].value
                new_description = modal.children[1].value

                print(f"New Title: {new_title}, New Description: {new_description}")

                # Обновление значений эмбеда
                self.embed.title = new_title
                self.embed.description = new_description

                # Отправка обновленного эмбеда
                try:
                    await interaction.message.edit(embed=self.embed)
                    print("Embed updated successfully.")
                except Exception as e:
                    print(f"Failed to update embed: {e}")

            modal.callback = callback

        except Exception as e:
            print(f"Error in edit_message: {e}")

    async def edit_thumbnail(self, interaction: Interaction) -> None:
        modal = Modal(title="Edit Embed Thumbnail")
        modal.add_item(
            TextInput(
                label="Thumbnail Url",
                default_value=self.embed.thumbnail.url,
                placeholder="Thumbnail you want to display in the embed",
                required=False,
            )
        )
        await interaction.response.send_modal(modal)

        # await modal.wait()

        async def callback(interaction):
            self.embed.set_thumbnail(url=modal.children[0].value)
            try:
                await interaction.message.edit(embed=self.embed)
                print("Embed updated successfully.")
            except Exception as e:
                print(f"Failed to update embed: {e}")

        modal.callback = callback

    async def edit_image(self, interaction: Interaction) -> None:
        modal = Modal(title="Edit Embed Image")
        modal.add_item(
            TextInput(
                label="Image Url",
                default_value=self.embed.image.url,
                placeholder="Image you want to display in the embed",
                required=False,
            )
        )
        await interaction.response.send_modal(modal)

        # await modal.wait()

        async def callback(interaction):
            self.embed.set_image(url=modal.children[0].value)
            try:
                await interaction.message.edit(embed=self.embed)
                print("Embed updated successfully.")
            except Exception as e:
                print(f"Failed to update embed: {e}")

        modal.callback = callback

    async def edit_footer(self, interaction: Interaction) -> None:
        modal = Modal(title="Edit Embed Footer")
        modal.add_item(
            TextInput(
                label="Footer Text",
                max_length=255,
                required=False,
                default_value=self.embed.footer.text,
                placeholder="Text you want to display on embed footer",
            )
        )
        modal.add_item(
            TextInput(
                label="Footer Icon",
                required=False,
                default_value=self.embed.footer.icon_url,
                placeholder="Icon you want to display on embed footer",
            )
        )
        await interaction.response.send_modal(modal)

        # await modal.wait()
        async def callback(interaction):
            self.embed.set_footer(
                text=modal.children[0].value, icon_url=modal.children[1].value
            )
            try:
                await interaction.message.edit(embed=self.embed)
                print("Embed updated successfully.")
            except Exception as e:
                print(f"Failed to update embed: {e}")

        modal.callback = callback

    async def edit_colour(self, interaction: Interaction) -> None:
        modal = Modal(title="Edit Embed Colour")
        modal.add_item(
            TextInput(
                label="Embed Colour",
                placeholder="The colour you want to display on embed (e.g: #303236)",
                max_length=20,
            )
        )
        await interaction.response.send_modal(modal)

        # await modal.wait()
        async def callback(interaction):
            try:
                colour = modal.children[0].value
                color = colour.replace("#", "")
                col = nextcord.Color(value=int(color, 16))
                col = col.to_rgb()
                self.embed.color = nextcord.Color.from_rgb(*col)
            except ValueError:
                await interaction.followup.send(
                    "Please provide a valid hex code.", ephemeral=True
                )
            try:
                await interaction.message.edit(embed=self.embed)
                print("Embed updated successfully.")
            except Exception as e:
                print(f"Failed to update embed: {e}")

        modal.callback = callback

    async def add_field(self, interaction: Interaction) -> None:
        if len(self.embed.fields) >= 25:
            return await interaction.response.send_message(
                "You cannot add more than 25 fields.", ephemeral=True
            )

        modal = Modal(title="Add a new field")
        modal.add_item(
            TextInput(
                label="Field Name",
                style=TextInputStyle.short,  # Здесь правильное использование стиля
                placeholder="The name you want to display on the field",
                max_length=255,
            )
        )
        modal.add_item(
            TextInput(
                label="Field Value",
                style=TextInputStyle.paragraph,  # Указание стиля для текста
                placeholder="The value you want to display on the field",
                max_length=2000,
            )
        )
        modal.add_item(
            TextInput(
                label="Field Inline (True/False)",
                style=TextInputStyle.short,  # Указание стиля для короткого текста
                default_value="True",
                placeholder="Should the field be inline? True or False",
                max_length=5,
            )
        )

        await interaction.response.send_modal(modal)

        # await modal.wait()

        async def callback(interaction):
            # Обработка введенных данных и обновление эмбеда
            try:
                inline = str(modal.children[2]).strip().lower() == "true"
            except ValueError:
                return await interaction.followup.send(
                    "Please provide a valid input for 'inline' (True or False).", ephemeral=True
                )

            self.embed.add_field(
                name=str(modal.children[0].value),
                value=str(modal.children[1].value),
                inline=inline
            )
            try:
                await interaction.message.edit(embed=self.embed)
                print("Embed updated successfully.")
            except Exception as e:
                print(f"Failed to update embed: {e}")

        modal.callback = callback

    async def remove_field(self, interaction: Interaction) -> None:
        if not self.embed.fields:
            return await interaction.response.send_message("There are no fields to remove.", ephemeral=True)

        field_options = [
            SelectOption(
                label=str(field.name)[:30],
                value=str(index),
                emoji="\U0001f5d1"
            )
            for index, field in enumerate(self.embed.fields)
        ]

        select = SelectPrompt(
            placeholder="Select a field to remove...",
            options=field_options,
            max_values=len(field_options),
            ephemeral=True
        )
        await interaction.response.send_message(view=select, ephemeral=True)

        async def callback(interaction):
            if vals := select.values:
                for value in vals:
                    self.embed.remove_field(int(value))
        select.select_callback = callback
