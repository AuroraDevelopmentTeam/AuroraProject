import random

import nextcord

possible_choices = ["brick", "knife", "evidence", "yandere", "tentacles"]

choice_emojis = {
    "brick": "brick",
    "knife": "knife",
    "evidence": "evidence",
    "yandere": "yandere",
    "tentacles": "tentacles"
}


def computer_random_choice() -> str:
    return random.choice(possible_choices)
