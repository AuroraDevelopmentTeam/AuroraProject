import sqlite3


def create_tickets_config_table() -> None:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    cursor.execute(
        f"""CREATE TABLE IF NOT EXISTS tickets_config (
        guild_id INTERGER, ticket_category INTERGER, ticket_archive INTERGER, ticket_support INTERGER
    )"""
    )
    db.commit()
    cursor.close()
    db.close()
    return
