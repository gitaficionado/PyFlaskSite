import sqlite3
from datetime import datetime
from werkzeug.security import check_password_hash, generate_password_hash

import click
from flask import current_app,g

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

def init_db():
    db = get_db()

    with current_app.open_resource('Database\\schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

@click.command('init-db')
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')


sqlite3.register_converter(
    "timestamp", lambda v: datetime.fromisoformat(v.decode())
)

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)

def addUser(username, password):
    get_db()
    try:
        g.db.execute(
            "INSERT INTO user (username, password) VALUES (?, ?)",
            (username, generate_password_hash(password)),
        )
        g.db.commit()
    except g.db.IntegrityError:
        return f"User {username} is already registered."
    else:
        return None
def getUserDataByName(username):
    get_db()
    return g.db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

def getUserDataById(user_id):
    get_db()
    return g.db.execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()

def saveScore(user_id, score):
    get_db()
    try:
        g.db.execute(
            "INSERT INTO leaderboard (userId, score) VALUES (?, ?)",
            (user_id, score),
        )
        g.db.commit()
    except g.db.IntegrityError:
        return f"problem occured."
    else:
        return None
