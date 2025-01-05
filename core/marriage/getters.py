from ..db_utils import fetch_one


GIFT_EMOJIS = {
    "gift_1": "🥕",
    "gift_2": "🧸",
    "gift_3": "<:cookie:1000701107611385886>",
    "gift_4": "<:7856lolipopcute:1000704880660455454>",
    "gift_5": "<a:9727magentalotusflower:1000698147892367390>",
    "gift_6": "🧣",
    "gift_7": "<:3603smallheartcake:1000705209124790292>",
    "gift_8": "<a:4680panda1:1000705939642535996>",
    "gift_9": "<a:6738_WaddlingDuck:1000699298763247656>",
    "gift_10": "<:7807meonguwuhearts:1000700312614608996>",
}

GIFT_NAMES = {
    "ru_ru": {
        "gift_1": "Морковка",
        "gift_2": "Мишка",
        "gift_3": "Печенька",
        "gift_4": "Лолипоп",
        "gift_5": "Цветок",
        "gift_6": "Шарфик",
        "gift_7": "Торт",
        "gift_8": "Панда",
        "gift_9": "Утка",
        "gift_10": "Кошка",
    },
    "en_us": {
        "gift_1": "Carrot",
        "gift_2": "Teddy bear",
        "gift_3": "Cookie",
        "gift_4": "Lolipop",
        "gift_5": "Flower",
        "gift_6": "Scarf",
        "gift_7": "Cake",
        "gift_8": "Panda",
        "gift_9": "Duck",
        "gift_10": "Cat",
    },
}

GIFT_PRICES = {
    "gift_1": 150,
    "gift_2": 1000,
    "gift_3": 250,
    "gift_4": 500,
    "gift_5": 750,
    "gift_6": 2500,
    "gift_7": 5000,
    "gift_8": 10500,
    "gift_9": 12000,
    "gift_10": 15000,
}


async def get_divorce_counter(guild_id: int, user_id: int) -> int:
    divorce_counter = await fetch_one(
        f"SELECT divorces FROM marriage WHERE guild_id = {guild_id} AND user_id = {user_id}"
    )
    return divorce_counter[0]

# TODO ничего не происходит если развод когда не женаты
async def get_user_pair_id(guild_id: int, user_id: int) -> int:
    pair_id = await fetch_one(
        f"SELECT pair_id FROM marriage WHERE guild_id = {guild_id} AND user_id = {user_id}"
    )
    return pair_id[0]


async def get_user_love_description(guild_id: int, user_id: int) -> str:
    love_description = await fetch_one(
        f"SELECT love_description FROM marriage WHERE guild_id = {guild_id} AND user_id = {user_id}"
    )
    return love_description[0]


async def get_user_marry_date(guild_id: int, user_id: int) -> str:
    date = await fetch_one(
        f"SELECT date FROM marriage WHERE guild_id = {guild_id} AND user_id = {user_id}"
    )
    return date[0]


async def get_user_loveroom_expire_date(guild_id: int, user_id: int) -> str:
    loveroom_expire_date = await fetch_one(
        f"SELECT loveroom_expire FROM marriage WHERE guild_id = {guild_id} AND user_id = {user_id}"
    )
    return loveroom_expire_date[0]


async def get_user_loveroom_id(guild_id: int, user_id: int) -> int:
    loveroom_id = await fetch_one(
        f"SELECT loveroom_id FROM marriage WHERE guild_id = {guild_id} AND user_id = {user_id}"
    )
    return loveroom_id[0]


async def get_family_money(guild_id: int, user_id: int) -> int:
    family_money = await fetch_one(
        f"SELECT family_money FROM marriage WHERE guild_id = {guild_id} AND user_id = {user_id}"
    )
    return family_money[0]


async def get_user_like_id(guild_id: int, user_id: int) -> int:
    like_id = await fetch_one(
        f"SELECT like_id FROM marriage WHERE guild_id = {guild_id} AND user_id = {user_id}"
    )
    return like_id[0]


async def get_user_gifts_price(guild_id: int, user_id: int) -> int:
    gift_price = await fetch_one(
        f"SELECT gift_price FROM gifts WHERE guild_id = {guild_id} AND user_id = {user_id}"
    )
    return gift_price[0]


async def get_user_gift_counter(guild_id: int, user_id: int, gift: str) -> int:
    gift_count = await fetch_one(
        f"SELECT {gift} FROM gifts WHERE guild_id = {guild_id} AND user_id = {user_id}"
    )
    return gift_count[0]


async def get_marriage_config_enable_loverooms(guild_id) -> bool:
    enable_loverooms = await fetch_one(
        f"SELECT enable_loverooms FROM marriage_config WHERE guild_id = {guild_id}"
    )
    return bool(enable_loverooms[0])


async def get_marriage_config_marriage_price(guild_id) -> int:
    marriage_price = await fetch_one(
        f"SELECT marriage_price FROM marriage_config WHERE guild_id = {guild_id}"
    )
    return marriage_price[0]


async def get_marriage_config_month_loveroom_price(guild_id) -> int:
    month_loveroom_price = await fetch_one(
        f"SELECT month_loveroom_price FROM marriage_config WHERE guild_id = {guild_id}"
    )
    return month_loveroom_price[0]


async def get_marriage_config_loveroom_category(guild_id) -> int:
    loveroom_category = await fetch_one(
        f"SELECT loveroom_category FROM marriage_config WHERE guild_id = {guild_id}"
    )
    return loveroom_category[0]

