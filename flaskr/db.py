import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext

# connecting to the database
def get_db():
    if 'db' not in g: #g is used to store data that might be accessed by multiple functions during the request
        g.db = sqlite3.connect( # sqlite3.connect establishes a connection to the file pointed at by the DATABASE configuration key. The file doesn't have to exist yet, and won't until we initialize the database later
            current_app.config['DATABASE'], # current_app is a proxy to the application handling the current request. Useful to access the application without needing to import it or if it can't be imported such as when using the application factory pattern (us)
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row # sqlite3.Row tells the connection to return rows that behave like dicts. This allows accessing the columns by name

    return g.db


def close_db(e=None): # checks if a connection was created. If it exists, it is closed. Futher down, we will tell our application about the close_db function in the application factory so that it is called after each request
    db = g.pop('db', None) # go over how this works

    if db is not None:
        db.close()


# python functions that will run schema.SQL commands 
def init_db():
    db = get_db() # establishes connection

    with current_app.open_resource('schema.sql') as f: #open_resource opens a resource file relative to rootpath
        db.executescript(f.read().decode('utf8'))


@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)

