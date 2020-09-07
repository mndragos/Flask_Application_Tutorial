__version__ = "0.1.0"

import os
from flask import Flask


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        DATABASE=os.path.join(app.instance_path, "flask_application_tutorial.userdata"),
    )
    if test_config is None:
        # Load the instance config, if exixts, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # load test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # database initialisation
    from . import db

    db.init_app(app)

    # register of blueprints
    from . import home
    from . import about
    from . import auth
    from . import my_dashboard
    from . import articles

    app.register_blueprint(home.bp)
    app.register_blueprint(about.bp)
    app.register_blueprint(auth.bp)
    app.register_blueprint(my_dashboard.bp)
    app.register_blueprint(articles.bp)

    return app
