import sqlite3


def update_ticket_category(guild_id: int, ticket_category: int) -> None:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    sql = "UPDATE tickets_config SET ticket_category = ? WHERE guild_id = ?"
    values = (ticket_category, guild_id)
    cursor.execute(sql, values)
    db.commit()
    cursor.close()
    db.close()
    return


def update_ticket_archive(guild_id: int, ticket_archive: int) -> None:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    sql = "UPDATE tickets_config SET ticket_archive = ? WHERE guild_id = ?"
    values = (ticket_archive, guild_id)
    cursor.execute(sql, values)
    db.commit()
    cursor.close()
    db.close()
    return


def update_ticket_support(guild_id: int, ticket_support: int) -> None:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    sql = "UPDATE tickets_config SET ticket_support = ? WHERE guild_id = ?"
    values = (ticket_support, guild_id)
    cursor.execute(sql, values)
    db.commit()
    cursor.close()
    db.close()
    return
