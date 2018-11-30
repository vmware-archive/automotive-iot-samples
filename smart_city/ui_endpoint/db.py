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
            '../cloud_db.db',
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
    db.execute( """CREATE TABLE IF NOT EXISTS events (client_side_id TEXT, user TEXT, event_type TEXT, event_timestamp INTEGER, gps_coord TEXT);""")

def read_events():
    """
    Reads last event from DB.
    """
    db = get_db()

    row = db.execute("""SELECT event_type, event_timestamp, gps_coord FROM events""").fetchall()

    return row

