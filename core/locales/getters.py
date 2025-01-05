import json
from ..db_utils import fetch_all

LOCALE_LIST = ["ru_ru", "en_us"]
LOCALE_CACHE = {}

def convert_locale_for_api(locale: str) -> str:
    return locale.replace('_', '-').lower()

async def preload_localizations():
    records = await fetch_all("SELECT guild_id, locale FROM locales")
    for record in records:
        print(record)
        LOCALE_CACHE[record[0]] = record[1]  # 0 - это guild_id, 1 - это locale

def get_guild_locale(guild_id: int) -> str:
    return LOCALE_CACHE.get(guild_id, "en_us")

def read_locale_file(locale: str) -> dict:
    try:
        with open(f"./locales/{locale}.json", mode="r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def get_msg_from_locale_by_key(guild_id: int, key: str) -> str:
    locale = get_guild_locale(guild_id)
    locales_file = read_locale_file(locale)
    return locales_file.get(key, {}).get("msg", "")

def localize_name(guild_id: int, key: str) -> str:
    locale = get_guild_locale(guild_id)
    locales_file = read_locale_file(locale)
    return locales_file.get(key, {}).get("name", "")

def get_keys_in_locale(guild_id: int, command_name: str) -> list:
    locale = get_guild_locale(guild_id)
    locales_file = read_locale_file(locale)
    return [key for key in locales_file.get(command_name, {}) if key not in ("name", "description")]

def get_keys_value_in_locale(guild_id: int, command_name: str) -> list:
    keys = get_keys_in_locale(guild_id, command_name)
    locale = get_guild_locale(guild_id)
    locales_file = read_locale_file(locale)
    return [locales_file.get(command_name, {}).get(key, "") for key in keys]

def get_localized_description(key: str) -> dict[str, str]:
    descs = []
    for locale in LOCALE_LIST:
        locales_file = read_locale_file(locale)
        descs.append(locales_file.get(key, {}).get("description", ""))
    return {"ru": descs[0], "en-US": descs[1]}

def get_localized_name(key: str) -> dict[str, str]:
    names = []
    for locale in LOCALE_LIST:
        locales_file = read_locale_file(locale)
        names.append(locales_file.get(key, {}).get("name", ""))
    return {"ru": names[0], "en-US": names[1]}

async def startup():
    await preload_localizations()
    print("Localizations preloaded:", LOCALE_CACHE)
