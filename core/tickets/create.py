import sqlite3


def create_tickets_config_table() -> None:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    cursor.execute(
        f"""CREATE TABLE IF NOT EXISTS tickets_config (
        guild_id INTEGER, ticket_category INTEGER, ticket_archive INTEGER, ticket_support INTEGER
    )"""
    )
    db.commit()
    cursor.close()
    db.close()
    return
