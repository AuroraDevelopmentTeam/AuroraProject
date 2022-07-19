import nextcord
from nextcord import ButtonStyle
from nextcord.ui import Button, View
from nextcord.ext import commands


def create_button(label: str, callback=False, disabled: bool = False):
    button = Button(label=label, style=ButtonStyle.secondary, disabled=disabled)
    if callback is not False:
        button.callback = callback
    return button
