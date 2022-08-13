import sqlite3


def create_badges_table() -> None:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    cursor.execute(
        f"""CREATE TABLE IF NOT EXISTS badges (
        guild_id INTERGER, user_id INTERGER, badge_1 BOOL, badge_2 BOOL, badge_3 BOOL, badge_4 BOOL, 
        badge_5 BOOL, badge_6 BOOL, badge_7 BOOL, badge_8 BOOL, badge_9 BOOL
    )"""
    )
    db.commit()
    cursor.close()
    db.close()
    return
