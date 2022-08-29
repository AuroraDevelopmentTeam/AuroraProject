import random
import nextcord

coin_toss = {
    "ru_ru": {0: "**Орёл**", 1: "**Решка**"},
    "en_us": {0: "**Heads**", 1: "**Tails**"},
}


def get_coin_toss(guild_locale):
    toss_a_coin = random.randint(0, 1)
    if toss_a_coin == 0:
        file = nextcord.File("./assets/heads.png", filename="coin.png")
    else:
        file = nextcord.File("./assets/tails.png", filename="coin.png")
    return file, coin_toss[guild_locale][toss_a_coin]
