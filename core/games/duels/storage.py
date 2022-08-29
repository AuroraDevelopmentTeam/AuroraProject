import random

BATTLE_PAGES = {
    "rat": {
        "focused_punch": {
            "cost": 3,
            "page_type": "attack",
            "attack_type": "chopping",
            "hits": 3,
            "hit_1": "attack",
            "hit_2": "attack",
            "hit_3": "attack",
            "damage_1": (5, 12),
            "damage_2": (5, 12),
            "damage_3": (5, 12),
            "image": "https://cdn.discordapp.com/attachments/1006417043899297833/1008398320395370507/unknown.png",
        },
        "hit_and_run": {
            "cost": 3,
            "page_type": "attack",
            "attack_type": "pierce",
            "hits": 3,
            "hit_1": "attack",
            "hit_2": "shield",
            "hit_3": "shield",
            "damage_1": (2, 11),
            "damage_2": (2, 6),
            "damage_3": (2, 6),
            "image": "https://cdn.discordapp.com/attachments/772385814483173398/1008622194005389362/unknown.png",
        },
        "light_defense": {
            "cost": 3,
            "page_type": "shield",
            "attack_type": "pierce",
            "hits": 3,
            "hit_1": "evade",
            "hit_2": "shield",
            "hit_3": "evade",
            "damage_1": (2, 12),
            "damage_2": (2, 8),
            "damage_3": (2, 12),
            "image": "https://cdn.discordapp.com/attachments/772385814483173398/1008622278050852964/unknown.png",
        },
    }
}
