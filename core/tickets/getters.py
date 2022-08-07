import sqlite3


def get_ticket_category(guild_id: int) -> int:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    ticket_category = cursor.execute(
        f"SELECT ticket_category FROM tickets_config WHERE guild_id = {guild_id}"
    ).fetchone()[0]
    cursor.close()
    db.close()
    return ticket_category


def get_ticket_archive(guild_id: int) -> int:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    ticket_archive = cursor.execute(
        f"SELECT ticket_archive FROM tickets_config WHERE guild_id = {guild_id}"
    ).fetchone()[0]
    cursor.close()
    db.close()
    return ticket_archive


def get_ticket_support(guild_id: int) -> int:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    ticket_support = cursor.execute(
        f"SELECT ticket_support FROM tickets_config WHERE guild_id = {guild_id}"
    ).fetchone()[0]
    cursor.close()
    db.close()
    return ticket_support
