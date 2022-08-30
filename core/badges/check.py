import nextcord
from core.badges.update import update_user_badge_state
from core.badges.converters import DEVELOPERS, OUR_TEAM, TESTERS, BUG_HUNTERS
from core.stats.getters import get_user_messages_counter, get_user_time_in_voice
from core.levels.getters import get_user_level
from core.money.getters import get_user_balance
from core.honor.getters import get_user_honor_level
from core.marriage.getters import get_user_pair_id


def check_badges(guild_id: int, user: nextcord.Member):
    if user.id in DEVELOPERS:
        update_user_badge_state(guild_id, user.id, "badge_1", True)
    if user.id in OUR_TEAM:
        update_user_badge_state(guild_id, user.id, "badge_2", True)
    if user.id in TESTERS:
        update_user_badge_state(guild_id, user.id, "badge_6", True)
    level = get_user_level(guild_id, user.id)
    time_in_voice = int(get_user_time_in_voice(guild_id, user.id)) / 3600
    messages = get_user_messages_counter(guild_id, user.id)
    if level >= 10 and time_in_voice >= 100 and messages >= 1000:
        update_user_badge_state(guild_id, user.id, "badge_3", True)
    money = get_user_balance(guild_id, user.id)
    if money >= 1000000:
        update_user_badge_state(guild_id, user.id, "badge_4", True)
    honor = get_user_honor_level(user.id)
    if honor >= 5:
        update_user_badge_state(guild_id, user.id, "badge_5", True)
    if user.id in BUG_HUNTERS:
        update_user_badge_state(guild_id, user.id, "badge_7", True)
    if get_user_pair_id(guild_id, user.id) != 0:
        update_user_badge_state(guild_id, user.id, "badge_9", True)
