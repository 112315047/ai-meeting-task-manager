import sqlite3
import os
import logging
from flask import g, current_app

logger = logging.getLogger(__name__)

DATABASE_URL = os.environ.get('DATABASE_URL', 'database.db')

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            DATABASE_URL
        )
        g.db.row_factory = sqlite3.Row
    return g.db

def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

def init_db():
    db = get_db()
    
    schema = """
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT,
        status TEXT DEFAULT 'pending', -- pending, in_progress, completed
        assignee TEXT,
        due_date TIMESTAMP,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """
    db.executescript(schema)
    logger.info("Initialized the SQLite database.")

def init_app(app):
    app.teardown_appcontext(close_db)
    
    # Simple way to initialize DB on first run or optionally add an internal command
    with app.app_context():
        # Usually it's better to do this in a CLI command, but for simplicity here we just run it on startup
        init_db()

