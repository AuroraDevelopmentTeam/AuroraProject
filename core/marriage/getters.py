import sqlite3

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


def get_divorce_counter(guild_id: int, user_id: int) -> int:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    divorce_counter = cursor.execute(
        f"SELECT divorces FROM marriage WHERE guild_id = {guild_id} AND user_id = {user_id}"
    ).fetchone()[0]
    cursor.close()
    db.close()
    return divorce_counter


def get_user_pair_id(guild_id: int, user_id: int) -> int:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    pair_id = cursor.execute(
        f"SELECT pair_id FROM marriage WHERE guild_id = {guild_id} AND user_id = {user_id}"
    ).fetchone()[0]
    cursor.close()
    db.close()
    return pair_id


def get_user_love_description(guild_id: int, user_id: int) -> str:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    love_description = cursor.execute(
        f"SELECT love_description FROM marriage WHERE guild_id = {guild_id} AND user_id = {user_id}"
    ).fetchone()[0]
    cursor.close()
    db.close()
    return love_description


def get_user_marry_date(guild_id: int, user_id: int) -> str:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    date = cursor.execute(
        f"SELECT date FROM marriage WHERE guild_id = {guild_id} AND user_id = {user_id}"
    ).fetchone()[0]
    cursor.close()
    db.close()
    return date


def get_user_loveroom_expire_date(guild_id: int, user_id: int) -> str:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    loveroom_expire_date = cursor.execute(
        f"SELECT loveroom_expire FROM marriage WHERE guild_id = {guild_id} AND user_id = {user_id}"
    ).fetchone()[0]
    cursor.close()
    db.close()
    return loveroom_expire_date


def get_user_loveroom_id(guild_id: int, user_id: int) -> int:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    loveroom_id = cursor.execute(
        f"SELECT loveroom_id FROM marriage WHERE guild_id = {guild_id} AND user_id = {user_id}"
    ).fetchone()[0]
    cursor.close()
    db.close()
    return loveroom_id


def get_family_money(guild_id: int, user_id: int) -> int:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    family_money = cursor.execute(
        f"SELECT family_money FROM marriage WHERE guild_id = {guild_id} AND user_id = {user_id}"
    ).fetchone()[0]
    cursor.close()
    db.close()
    return family_money


def get_user_like_id(guild_id: int, user_id: int) -> int:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    like_id = cursor.execute(
        f"SELECT like_id FROM marriage WHERE guild_id = {guild_id} AND user_id = {user_id}"
    ).fetchone()[0]
    cursor.close()
    db.close()
    return like_id


def get_user_gifts_price(guild_id: int, user_id: int) -> int:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    gift_price = cursor.execute(
        f"SELECT gift_price FROM gifts WHERE guild_id = {guild_id} AND user_id = {user_id}"
    ).fetchone()[0]
    cursor.close()
    db.close()
    return gift_price


def get_user_gift_counter(guild_id: int, user_id: int, gift: str) -> int:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    gift_count = cursor.execute(
        f"SELECT {gift} FROM gifts WHERE guild_id = {guild_id} AND user_id = {user_id}"
    ).fetchone()[0]
    cursor.close()
    db.close()
    return gift_count


def get_marriage_config_enable_loverooms(guild_id) -> bool:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    enable_loverooms = cursor.execute(
        f"SELECT enable_loverooms FROM marriage_config WHERE guild_id = {guild_id}"
    ).fetchone()[0]
    cursor.close()
    db.close()
    return bool(enable_loverooms)


def get_marriage_config_marriage_price(guild_id) -> int:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    marriage_price = cursor.execute(
        f"SELECT marriage_price FROM marriage_config WHERE guild_id = {guild_id}"
    ).fetchone()[0]
    cursor.close()
    db.close()
    return marriage_price


def get_marriage_config_month_loveroom_price(guild_id) -> int:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    month_loveroom_price = cursor.execute(
        f"SELECT month_loveroom_price FROM marriage_config WHERE guild_id = {guild_id}"
    ).fetchone()[0]
    cursor.close()
    db.close()
    return month_loveroom_price


def get_marriage_config_loveroom_category(guild_id) -> int:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    loveroom_category = cursor.execute(
        f"SELECT loveroom_category FROM marriage_config WHERE guild_id = {guild_id}"
    ).fetchone()[0]
    cursor.close()
    db.close()
    return loveroom_category

