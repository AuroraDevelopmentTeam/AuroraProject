import random

from core.games.duels.storage import BATTLE_PAGES


def who_first() -> int:
    return random.randint(0, 1)


def play_card(player_class: str, battle_page: str):
    doct = {}
    if BATTLE_PAGES[player_class][battle_page]["page_type"] == "attack":
        for i in range(BATTLE_PAGES[player_class][battle_page]["hits"]):
            if BATTLE_PAGES[player_class][battle_page][f"hit_{i + 1}"] == "attack":
                if BATTLE_PAGES[player_class][battle_page]["attack_type"] == "chopping":
                    doct.update({i: ["chop",
                                     random.randint(BATTLE_PAGES[player_class][battle_page][f"damage_{i + 1}"][0],
                                                    BATTLE_PAGES[player_class][battle_page][f"damage_{i + 1}"][1])]})
                elif BATTLE_PAGES[player_class][battle_page]["attack_type"] == "pierce":
                    doct.update({i: ["pierce",
                                     random.randint(BATTLE_PAGES[player_class][battle_page][f"damage_{i + 1}"][0],
                                                    BATTLE_PAGES[player_class][battle_page][f"damage_{i + 1}"][1])]})
            elif BATTLE_PAGES[player_class][battle_page][f"hit_{i + 1}"] == "shield":
                doct.update({i: ["shield",
                                 random.randint(BATTLE_PAGES[player_class][battle_page][f"damage_{i + 1}"][0],
                                                BATTLE_PAGES[player_class][battle_page][f"damage_{i + 1}"][1])]})
            elif BATTLE_PAGES[player_class][battle_page][f"hit_{i + 1}"] == "evade":
                doct.update({i: ["evade",
                                 random.randint(BATTLE_PAGES[player_class][battle_page][f"damage_{i + 1}"][0],
                                                BATTLE_PAGES[player_class][battle_page][f"damage_{i + 1}"][1])]})
    if BATTLE_PAGES[player_class][battle_page]["page_type"] == "shield":
        for i in range(BATTLE_PAGES[player_class][battle_page]["hits"]):
            if BATTLE_PAGES[player_class][battle_page][f"hit_{i + 1}"] == "shield":
                doct.update({i: ["shield",
                                 random.randint(BATTLE_PAGES[player_class][battle_page][f"damage_{i + 1}"][0],
                                                BATTLE_PAGES[player_class][battle_page][f"damage_{i + 1}"][1])]})
            elif BATTLE_PAGES[player_class][battle_page][f"hit_{i + 1}"] == "evade":
                doct.update({i: ["evade",
                                 random.randint(BATTLE_PAGES[player_class][battle_page][f"damage_{i + 1}"][0],
                                                BATTLE_PAGES[player_class][battle_page][f"damage_{i + 1}"][1])]})

    return doct


player_1 = play_card("rat", "focused_punch")
player_2 = play_card("rat", "focused_punch")


def players_compare(player_1_entry, player_2_entry, who_first: int, player_1_hp, player_2_hp):
    if who_first == 0:
        if len(player_1_entry) == len(player_2_entry):
            while player_1_hp > 0 and player_2_hp > 0:
                for i in range(len(player_1_entry)):
                    if player_2_hp <= 0 or player_1_hp <= 0:
                        print(player_1[i], player_2[i])
                        print(player_1_hp, player_2_hp)
                    if player_1[i][0] == 'chop':
                        if player_2[i][0] == 'shield':
                            player_1[i][1] -= player_2[i][1]
                            if player_1[i][1] < 0:
                                player_1[i][1] = 0
                        elif player_2[i][0] == 'evade':
                            if player_2[i][1] >= player_1[i][1]:
                                player_1[i][1] = 0
                            player_1_hp -= player_2[i][1]
                        if player_2_hp > 0 and player_1_hp > 0:
                            player_2_hp -= player_1[i][1]
                        if player_2_hp <= 0:
                            return print("player_1_win")
                        if player_2[i][0] == 'chop':
                            player_1_hp -= player_2[i][1]
                        if player_2[i][0] == 'pierce':
                            player_1_hp -= player_2[i][1]
                        print(player_1[i], player_2[i])
                        print(player_1_hp, player_2_hp)
                        if player_1_hp <= 0:
                            return print("player_2_win")
                    if player_1[i][0] == 'pierce':
                        if player_2[i][0] == 'shield':
                            player_2_hp -= int(player_1[i][1] / 2)
                            player_1[i][1] -= int(player_1[i][1] / 2)
                            player_1[i][1] -= player_2[i][1]
                            if player_1[i][1] < 0:
                                player_1[i][1] = 0
                        elif player_2[i][0] == 'evade':
                            if player_2[i][1] >= player_1[i][1]:
                                player_1[i][1] = 0
                            player_1_hp -= player_2[i][1]
                        if player_2_hp > 0 and player_1_hp > 0:
                            player_2_hp -= player_1[i][1]
                        if player_2_hp <= 0:
                            return print("player_1_win")
                        if player_2[i][0] == 'chop':
                            player_1_hp -= player_2[i][1]
                        elif player_2[i][0] == 'pierce':
                            player_1_hp -= player_2[i][1]
                        print(player_1[i], player_2[i])
                        print(player_1_hp, player_2_hp)
                        if player_1_hp <= 0:
                            return print("player_2_win")
                    if player_1[i][0] == 'shield':
                        if player_2[i][0] == 'shield':
                            player_2[i][1] = 0
                            player_1[i][1] = 0
                        elif player_2[i][0] == 'evade':
                            player_2[i][1] = 0
                            player_1[i][1] = 0
                        if player_2_hp > 0 and player_1_hp > 0:
                            player_2_hp -= player_1[i][1]
                        if player_2_hp <= 0:
                            return print("player_1_win")
                        if player_2[i][0] == 'chop':
                            if player_1[i][1] >= player_2[i][1]:
                                player_2[i][1] = 0
                            player_1_hp -= player_2[i][1]
                            player_2_hp -= player_1[i][1]
                        elif player_2[i][0] == 'pierce':
                            player_1_hp -= int(player_2[i][1] / 2)
                            player_2[i][1] -= int(player_2[i][1] / 2)
                            player_2[i][1] -= player_1[i][1]
                            if player_2[i][1] < 0:
                                player_2[i][1] = 0
                            player_1_hp -= player_2[i][1]
                        print(player_1[i], player_2[i])
                        print(player_1_hp, player_2_hp)
                        if player_1_hp <= 0:
                            return print("player_2_win")
                    if player_1[i][0] == 'evade':
                        if player_2[i][0] == 'shield':
                            player_2[i][1] = 0
                            player_1[i][1] = 0
                        elif player_2[i][0] == 'evade':
                            player_2[i][1] = 0
                            player_1[i][1] = 0
                        if player_2_hp > 0 and player_1_hp > 0:
                            player_2_hp -= player_1[i][1]
                        if player_2_hp <= 0:
                            return print("player_1_win")
                        if player_2[i][0] == 'chop':
                            player_2[i][1] -= player_1[i][1]
                            if player_2[i][1] < 0:
                                player_2[i][1] = 0
                                player_2_hp -= player_2[i][1]
                            player_1_hp -= player_2[i][1]
                        elif player_2[i][0] == 'pierce':
                            player_2[i][1] -= player_1[i][1]
                            if player_2[i][1] < 0:
                                player_2[i][1] = 0
                                player_2_hp -= player_2[i][1]
                            player_1_hp -= player_2[i][1]
                        print(player_1[i], player_2[i])
                        print(player_1_hp, player_2_hp)
                        if player_1_hp <= 0:
                            return print("player_2_win")
    print(player_1_hp, player_2_hp)


players_compare(player_1, player_2, 0, 100, 100)
