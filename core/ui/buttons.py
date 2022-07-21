import typing

import nextcord
from nextcord import ButtonStyle, Interaction
from nextcord.ui import Button, View
from nextcord.ext import commands


def create_button(label: str, callback=False, disabled: bool = False):
    button = Button(label=label, style=ButtonStyle.secondary, disabled=disabled)
    if callback is not False:
        button.callback = callback
    return button


class ViewAuthorCheck(View):
    def __init__(self, author: typing.Union[nextcord.Member, nextcord.User]):
        self.author = author
        super().__init__()

    async def interaction_check(self, interaction: Interaction) -> bool:
        if interaction.user != self.author:
            return False
        return True