import sqlite3


def create_badges_table() -> None:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    cursor.execute(
        f"""CREATE TABLE IF NOT EXISTS badges (
        guild_id INTERGER, user_id INTERGER, badge_1, INTERGER, badge_2 INTERGER, badge_3 INTERGER, badge_4 INTERGER, 
        badge_5 INTERGER, badge_6 INTERGER, badge_7 INTERGER, badge_8 INTERGER, badge_9 INTERGER
    )"""
    )
    db.commit()
    cursor.close()
    db.close()
    return
