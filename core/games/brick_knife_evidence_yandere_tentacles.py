import random

import nextcord
from nextcord import Interaction
from nextcord.ui import View

from core.ui.buttons import create_button
from core.embeds import DEFAULT_BOT_COLOR

possible_choices = ["brick", "knife", "evidence", "yandere", "tentacles"]

choice_emojis = {
    "brick": "🧱",
    "knife": "🔪",
    "evidence": "<:evidence:998620951644221462>",
    "yandere": "<a:yanderestalk:998622116746371092>",
    "tentacles": "<a:9088_Tentacles:998620562903543950>",
}


def computer_random_choice() -> str:
    return random.choice(possible_choices)


def emojify_choice(choice) -> str:
    return choice_emojis[choice]


def create_starting_view() -> View:
    brick_button = create_button("brick", brick_button_callback, False)
    brick_button.emoji = emojify_choice("brick")
    knife_button = create_button("knife", knife_button_callback, False)
    knife_button.emoji = emojify_choice("knife")
    evidence_button = create_button("evidence", evidence_button_callback, False)
    evidence_button.emoji = emojify_choice("evidence")
    yandere_button = create_button("yandere", yandere_button_callback, False)
    yandere_button.emoji = emojify_choice("yandere")
    tentacles = create_button("tentacles", tentacles_button_callback, False)
    tentacles.emoji = emojify_choice("tentacles")
    view = View()
    view.add_item(brick_button)
    view.add_item(knife_button)
    view.add_item(evidence_button)
    view.add_item(yandere_button)
    view.add_item(tentacles)
    return view


def check_win(player_choice: str, computer_choice: str) -> bool:
    result = {
        ("brick", "brick"): None,
        ("brick", "knife"): True,
        ("brick", "evidence"): False,
        ("brick", "yandere"): False,
        ("brick", "tentacles"): True,
        ("knife", "brick"): False,
        ("knife", "knife"): None,
        ("knife", "evidence"): True,
        ("knife", "yandere"): False,
        ("knife", "tentacles"): True,
        ("evidence", "brick"): True,
        ("evidence", "knife"): False,
        ("evidence", "evidence"): None,
        ("evidence", "yandere"): True,
        ("evidence", "tentacles"): False,
        ("yandere", "brick"): True,
        ("yandere", "knife"): True,
        ("yandere", "evidence"): False,
        ("yandere", "yandere"): None,
        ("yandere", "tentacles"): False,
        ("tentacles", "brick"): False,
        ("tentacles", "knife"): False,
        ("tentacles", "evidence"): True,
        ("tentacles", "yandere"): True,
        ("tentacles", "tentacles"): None,
    }
    return result[player_choice, computer_choice]


def get_phrase(player_choice: str, computer_choice: str) -> str:
    phrases = {
        "ru_ru": {("brick", "brick"): "Кирпич на кирпич! Вау, строим дом"},
        "en_us": {
            ("brick", "brick"): "Brick on brick! Wow, are we trying build a house?",
            (
                "brick",
                "knife",
            ): "Brick and knife. Uhm.. Hey, Knife, can you at least try? Seems no",
            ("brick", "evidence"): "Brick and evidence. Just like paper and rock",
            ("brick", "yandere"): "Brick and yandere. New weapon for yandere",
            (
                "brick",
                "tentacles",
            ): "Brick and tentacles. Tentacles can't do anything to a brick!?",
            (
                "knife",
                "brick",
            ): "Brick and knife. Uhm.. Hey, Knife, can you at least try? Seems no",
            ("knife", "knife"): "Knife and knife. CUT-CUT-CUT",
            ("knife", "evidence"): "Knife and evidence. Like paper and scissors",
            (
                "knife",
                "yandere",
            ): "Knife and yandere. Knife is yandere's favorite weapon",
            (
                "knife",
                "tentacles",
            ): "Knife and tentacles. Dear, we're having seafood for dinner tonight",
            ("evidence", "brick"): "Brick and evidence. Just like paper and rock",
            ("evidence", "knife"): "Knife and evidence. Like paper and scissors",
            (
                "evidence",
                "evidence",
            ): "Evidence and evidence. Now yandere really don't stand a chance",
            ("evidence", "yandere"): "Evidence and yandere. Now her sempai know truth",
            (
                "evidence",
                "tentacles",
            ): "Evidence and tentacles. Now this is not evidence, but just a paper ball",
            ("yandere", "brick"): "Brick and yandere. New weapon for yandere",
            (
                "yandere",
                "knife",
            ): "Knife and yandere. Knife is yandere's favorite weapon",
            ("yandere", "evidence"): "Evidence and yandere. Now her sempai know truth",
            ("yandere", "yandere"): "Yandere and yandere. Senpai! Senpai! Senpai!",
            ("yandere", "tentacles"): "Yandere and tentacles. Is this new hentai?",
            (
                "tentacles",
                "brick",
            ): "Brick and tentacles. Tentacles can't do anything to a brick!?",
            (
                "tentacles",
                "knife",
            ): "Knife and tentacles. Dear, we're having seafood for dinner tonight",
            (
                "tentacles",
                "evidence",
            ): "Evidence and tentacles. Now this is not evidence, but just a paper ball",
            ("tentacles", "yandere"): "Yandere and tentacles. Is this new hentai?",
            (
                "tentacles",
                "tentacles",
            ): "Tentacles on tentacles, tentacles on tentacles and tentacles in tentacles at "
            "tentacles under tentacles behind tentacles, etc, just draw and many tentacles",
        },
    }
    return phrases["en_us"][player_choice, computer_choice]


def create_starting_embed(title, description) -> nextcord.Embed:
    embed = nextcord.Embed(
        title=title, description=description, color=DEFAULT_BOT_COLOR
    )
    return embed


def create_final_view() -> View:
    brick_button = create_button("brick", False, True)
    brick_button.emoji = emojify_choice("brick")
    knife_button = create_button("knife", False, True)
    knife_button.emoji = emojify_choice("knife")
    evidence_button = create_button("evidence", False, True)
    evidence_button.emoji = emojify_choice("evidence")
    yandere_button = create_button("yandere", False, True)
    yandere_button.emoji = emojify_choice("yandere")
    tentacles = create_button("tentacles", False, True)
    tentacles.emoji = emojify_choice("tentacles")
    view = View()
    view.add_item(brick_button)
    view.add_item(knife_button)
    view.add_item(evidence_button)
    view.add_item(yandere_button)
    view.add_item(tentacles)
    return view


def create_final_embed(title: str, description: str) -> nextcord.Embed:
    embed = nextcord.Embed(
        title=title, description=description, color=DEFAULT_BOT_COLOR
    )
    return embed


async def brick_button_callback(interaction: Interaction):
    player_choice = "brick"
    computer_choice = computer_random_choice()
    is_win = check_win(player_choice, computer_choice)
    phrase = get_phrase(player_choice, computer_choice)
    if is_win is True:
        embed = create_final_embed(
            "Brick Knife Evidence Yandere Tentacles", f"**Player** win"
        )
        embed.add_field(
            name="Your choice:", value=f"{emojify_choice(player_choice)}", inline=True
        )
        embed.add_field(name="My choice:", value=f"{emojify_choice(computer_choice)}")
        embed.set_footer(text=phrase)
        view = create_final_view()
        await interaction.message.edit(embed=embed, view=view)
    if is_win is None:
        embed = create_final_embed(
            "Brick Knife Evidence Yandere Tentacles", f"**Draw**"
        )
        embed.add_field(
            name="Your choice:", value=f"{emojify_choice(player_choice)}", inline=True
        )
        embed.add_field(name="My choice:", value=f"{emojify_choice(computer_choice)}")
        embed.set_footer(text=phrase)
        view = create_final_view()
        await interaction.message.edit(embed=embed, view=view)
    if is_win is False:
        embed = create_final_embed(
            "Brick Knife Evidence Yandere Tentacles", f"**Player** loose"
        )
        embed.add_field(
            name="Your choice:", value=f"{emojify_choice(player_choice)}", inline=True
        )
        embed.add_field(name="My choice:", value=f"{emojify_choice(computer_choice)}")
        embed.set_footer(text=phrase)
        view = create_final_view()
        await interaction.message.edit(embed=embed, view=view)


async def knife_button_callback(interaction: Interaction):
    player_choice = "knife"
    computer_choice = computer_random_choice()
    is_win = check_win(player_choice, computer_choice)
    phrase = get_phrase(player_choice, computer_choice)
    if is_win is True:
        embed = create_final_embed(
            "Brick Knife Evidence Yandere Tentacles", f"**Player** win"
        )
        embed.add_field(
            name="Your choice:", value=f"{emojify_choice(player_choice)}", inline=True
        )
        embed.add_field(name="My choice:", value=f"{emojify_choice(computer_choice)}")
        embed.set_footer(text=phrase)
        view = create_final_view()
        await interaction.message.edit(embed=embed, view=view)
    if is_win is None:
        embed = create_final_embed(
            "Brick Knife Evidence Yandere Tentacles", f"**Draw**"
        )
        embed.add_field(
            name="Your choice:", value=f"{emojify_choice(player_choice)}", inline=True
        )
        embed.add_field(name="My choice:", value=f"{emojify_choice(computer_choice)}")
        embed.set_footer(text=phrase)
        view = create_final_view()
        await interaction.message.edit(embed=embed, view=view)
    if is_win is False:
        embed = create_final_embed(
            "Brick Knife Evidence Yandere Tentacles", f"**Player** loose"
        )
        embed.add_field(
            name="Your choice:", value=f"{emojify_choice(player_choice)}", inline=True
        )
        embed.add_field(name="My choice:", value=f"{emojify_choice(computer_choice)}")
        embed.set_footer(text=phrase)
        view = create_final_view()
        await interaction.message.edit(embed=embed, view=view)


async def evidence_button_callback(interaction: Interaction):
    player_choice = "evidence"
    computer_choice = computer_random_choice()
    is_win = check_win(player_choice, computer_choice)
    phrase = get_phrase(player_choice, computer_choice)
    if is_win is True:
        embed = create_final_embed(
            "Brick Knife Evidence Yandere Tentacles", f"**Player** win"
        )
        embed.add_field(
            name="Your choice:", value=f"{emojify_choice(player_choice)}", inline=True
        )
        embed.add_field(name="My choice:", value=f"{emojify_choice(computer_choice)}")
        embed.set_footer(text=phrase)
        view = create_final_view()
        await interaction.message.edit(embed=embed, view=view)
    if is_win is None:
        embed = create_final_embed(
            "Brick Knife Evidence Yandere Tentacles", f"**Draw**"
        )
        embed.add_field(
            name="Your choice:", value=f"{emojify_choice(player_choice)}", inline=True
        )
        embed.add_field(name="My choice:", value=f"{emojify_choice(computer_choice)}")
        embed.set_footer(text=phrase)
        view = create_final_view()
        await interaction.message.edit(embed=embed, view=view)
    if is_win is False:
        embed = create_final_embed(
            "Brick Knife Evidence Yandere Tentacles", f"**Player** loose"
        )
        embed.add_field(
            name="Your choice:", value=f"{emojify_choice(player_choice)}", inline=True
        )
        embed.add_field(name="My choice:", value=f"{emojify_choice(computer_choice)}")
        embed.set_footer(text=phrase)
        view = create_final_view()
        await interaction.message.edit(embed=embed, view=view)


async def yandere_button_callback(interaction: Interaction):
    player_choice = "yandere"
    computer_choice = computer_random_choice()
    is_win = check_win(player_choice, computer_choice)
    phrase = get_phrase(player_choice, computer_choice)
    if is_win is True:
        embed = create_final_embed(
            "Brick Knife Evidence Yandere Tentacles", f"**Player** win"
        )
        embed.add_field(
            name="Your choice:", value=f"{emojify_choice(player_choice)}", inline=True
        )
        embed.add_field(name="My choice:", value=f"{emojify_choice(computer_choice)}")
        embed.set_footer(text=phrase)
        view = create_final_view()
        await interaction.message.edit(embed=embed, view=view)
    if is_win is None:
        embed = create_final_embed(
            "Brick Knife Evidence Yandere Tentacles", f"**Draw**"
        )
        embed.add_field(
            name="Your choice:", value=f"{emojify_choice(player_choice)}", inline=True
        )
        embed.add_field(name="My choice:", value=f"{emojify_choice(computer_choice)}")
        embed.set_footer(text=phrase)
        view = create_final_view()
        await interaction.message.edit(embed=embed, view=view)
    if is_win is False:
        embed = create_final_embed(
            "Brick Knife Evidence Yandere Tentacles", f"**Player** loose"
        )
        embed.add_field(
            name="Your choice:", value=f"{emojify_choice(player_choice)}", inline=True
        )
        embed.add_field(name="My choice:", value=f"{emojify_choice(computer_choice)}")
        embed.set_footer(text=phrase)
        view = create_final_view()
        await interaction.message.edit(embed=embed, view=view)


async def tentacles_button_callback(interaction: Interaction):
    player_choice = "tentacles"
    computer_choice = computer_random_choice()
    is_win = check_win(player_choice, computer_choice)
    phrase = get_phrase(player_choice, computer_choice)
    if is_win is True:
        embed = create_final_embed(
            "Brick Knife Evidence Yandere Tentacles", f"**Player** win"
        )
        embed.add_field(
            name="Your choice:", value=f"{emojify_choice(player_choice)}", inline=True
        )
        embed.add_field(name="My choice:", value=f"{emojify_choice(computer_choice)}")
        embed.set_footer(text=phrase)
        view = create_final_view()
        await interaction.message.edit(embed=embed, view=view)
    if is_win is None:
        embed = create_final_embed(
            "Brick Knife Evidence Yandere Tentacles", f"**Draw**"
        )
        embed.add_field(
            name="Your choice:", value=f"{emojify_choice(player_choice)}", inline=True
        )
        embed.add_field(name="My choice:", value=f"{emojify_choice(computer_choice)}")
        embed.set_footer(text=phrase)
        view = create_final_view()
        await interaction.message.edit(embed=embed, view=view)
    if is_win is False:
        embed = create_final_embed(
            "Brick Knife Evidence Yandere Tentacles", f"**Player** loose"
        )
        embed.add_field(
            name="Your choice:", value=f"{emojify_choice(player_choice)}", inline=True
        )
        embed.add_field(name="My choice:", value=f"{emojify_choice(computer_choice)}")
        embed.set_footer(text=phrase)
        view = create_final_view()
        await interaction.message.edit(embed=embed, view=view)
