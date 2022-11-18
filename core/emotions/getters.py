import sqlite3


def get_emotions_for_money_state(guild_id: int) -> bool:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    emotions_for_money_state = cursor.execute(
        f"SELECT emotions_for_money_state FROM emotions_cost WHERE guild_id = {guild_id}"
    ).fetchone()[0]
    db.commit()
    cursor.close()
    db.close()
    return bool(emotions_for_money_state)


def get_emotions_cost(guild_id: int) -> int:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    emotions_cost = cursor.execute(
        f"SELECT cost FROM emotions_cost WHERE guild_id = {guild_id}"
    ).fetchone()[0]
    db.commit()
    cursor.close()
    db.close()
    return emotions_cost


def is_emotion_free(guild_id: int) -> bool:
    emotions_for_money_state = get_emotions_for_money_state(guild_id)
    if emotions_for_money_state is False:
        return True
    else:
        emotions_cost = get_emotions_cost(guild_id)
        if emotions_cost == 0:
            return True
        else:
            return False

