# __init__.py contains the application factory
# and tells Python that the flaskr directory should
# be treated as a package

import os # provides functions for interacting with the operating system

from flask import Flask


def create_app(test_config=None): # application factory function
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True) 
    #__name__ is the name of the current module
    # instance_relative_config=True tells the app that
    # configuration files are relative to the instance folder
    # The instance folder is located outside of flaskr package and can hold local data that shouldn't be commited to version control (e.g. configuration secrets and the db file) 
    app.config.from_mapping( # sets some default configuration that the app will use
        SECRET_KEY='dev', # used by Flask and extensions to keep data safe. Should be overridden with a random value when deploying
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'), # path where the SQLite db file will be saved. app.instance_path holds the path to the instance folder
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True) # overrides the default configuration with values taken from the config.py file in the instance folder if it exists
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config) # teest_config can also be passed to the factory, and will be used instead of the instance configuration. This is so test we write later can be configured independently of any dev values we have configured

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path) #app.instance_path holds the path to the instance folder
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/hello') # creates a simple route so we can see the application working before getting to the rest of the tutorial. Creates a connection between the URL /hello and a function that returns the string Hello, World!
    # route - decorate a view function to register it with the given URL rule and options
    def hello():
        return 'Hello, World!'

    from . import db
    db.init_app(app)

    # import and register auth blueprint
    from . import auth
    app.register_blueprint(auth.bp)

    # import and register blog blueprint
    from . import blog
    app.register_blueprint(blog.bp)
    app.add_url_rule('/', endpoint='index')

    return app