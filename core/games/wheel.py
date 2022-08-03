import random

from core.embeds import DEFAULT_BOT_COLOR

import nextcord
from nextcord import Asset

MULTIPLIERS = [
    0,
    0.1,
    0.1,
    0.2,
    0.1,
    0.2,
    0.3,
    0.4,
    0.5,
    0.6,
    0.7,
    0.8,
    0.9,
    1.2,
    1.3,
    1.5,
    1.7,
    1.9,
    2.0,
    2.2,
]

arrow_directions = {
    0: "↖️",
    1: "⬆️️",
    2: "↗️",
    3: "➡️️",
    4: "↘️️",
    5: "⬇️️",
    6: "↙️️",
    7: "⬅️️",
}


def initialize_multipliers() -> list:
    return [random.choice(MULTIPLIERS) for i in range(8)]


def spin_wheel() -> int:
    return random.randint(0, 7)


def get_multiplier(multipliers: list, index: int) -> int:
    return multipliers[index]


def get_direction(index: int) -> str:
    return arrow_directions[index]


def construct_wheel_embed(
    title: str, multipliers: list, direction: str, footer_text: str, footer_url: Asset
) -> nextcord.Embed:
    wheel = nextcord.Embed(
        title=title,
        description=f"\n\n\n**|⠀⠀{multipliers[0]}⠀⠀|⠀⠀{multipliers[1]}⠀⠀|⠀⠀{multipliers[2]}⠀⠀|**\n\n\n"
        f"**|⠀⠀{multipliers[3]}⠀⠀|⠀⠀{direction}⠀⠀|⠀⠀{multipliers[4]}⠀⠀|**\n\n\n"
        f"**|⠀⠀{multipliers[5]}⠀⠀|⠀⠀{multipliers[6]}⠀⠀|⠀⠀{multipliers[7]}⠀⠀|**",
        color=DEFAULT_BOT_COLOR,
    )
    wheel.set_footer(text=footer_text, icon_url=footer_url)
    return wheel
