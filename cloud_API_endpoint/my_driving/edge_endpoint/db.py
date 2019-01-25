import sqlite3

from flask import current_app, g

def get_db():
    """
    Connect to the application's configured database. The connection
    is unique for each request and will be reused if this is called
    again.
    """
    if 'db' not in g:
        g.db = sqlite3.connect(
            '../data/cloud_db.db',
            detect_types=sqlite3.PARSE_DECLTYPES
            )
        g.db.row_factory = sqlite3.Row
        initialize_DB(g.db)
    return g.db

def initialize_DB(db):
    """
    Creating event table if it doesn't already exist.

    The event table has two keys:
    1-A key generated on the edge gateway when an event detected.
    2-The sqlite3 rowid: http://www.sqlitetutorial.net/sqlite-autoincrement/
    """
    db.execute( """CREATE TABLE IF NOT EXISTS events (client_side_id TEXT, user TEXT, event_timestamp INTEGER, distance TEXT, fuel TEXT);""")

def write_event(json_data):
    """
    Inserts data passed in argument.
    """
    db = get_db()

    row_to_insert = [
        json_data["client_side_id"],
        json_data["user"],
        int(json_data["event_timestamp"]),
        json_data["distance"],
        json_data["fuel"]
        ]

    db.execute("""INSERT OR REPLACE INTO events VALUES(?,?,?,?,?)""",row_to_insert)
    db.commit()



