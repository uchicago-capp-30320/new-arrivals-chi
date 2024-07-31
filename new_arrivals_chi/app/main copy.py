"""Project: new_arrivals_chi.

File name: main.py
Associated Files:
    Templates: base.html, home.html, legal.html, health.html,
    health_search.html, dashboard.html, login.html, info.html.

Runs primary flask application for Chicago's new arrivals' portal.

Methods:
    * home — Route to homepage of application.
    * dashboard - Route to user's dashboard.
    * legal - Route to legal portion of application.
"""
from flask import Flask, Blueprint, render_template, request, g
from flask_babel import Babel, lazy_gettext as _
from datetime import timedelta
import os
from new_arrivals_chi.app.database import db
from new_arrivals_chi.app.authorize_routes import authorize
from flask_migrate import Migrate
from flask_login import LoginManager, current_user
import bleach
from markupsafe import escape
from new_arrivals_chi.app.utils import load_neighborhoods, validate_email_syntax, validate_phone_number, create_temp_pwd
from new_arrivals_chi.app.data_handler import create_user, create_organization_profile, extract_organization
from dotenv import load_dotenv

migrate = Migrate()
load_dotenv()

app = Flask(__name__)
babel = Babel(app)

def get_locale():
    lang = request.args.get('lang', 'es')  # Default to Spanish
    print(f"Selected language: {lang}")  # Debugging line
    g.current_lang = lang
    return lang

babel.init_app(app, locale_selector=get_locale)

@app.context_processor
def inject_locale():
    return dict(get_locale=get_locale)

# Define the blueprint
main = Blueprint("main", __name__, static_folder="static")

# Define routes within the blueprint
@main.route("/")
def home():
    return render_template('home.html')

@main.route("/about")
def about():
    return render_template("about.html")

# Define other routes similarly within the `main` blueprint

# Function to create the Flask app
def create_app(config_override=None):
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL", default="sqlite:///:memory:")
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["REMEMBER_COOKIE_DURATION"] = timedelta(hours=12)

    # Load neighborhoods from file and store in app config
    app.config["NEIGHBORHOODS"] = load_neighborhoods()

    # Configure Babel
    app.config['BABEL_DEFAULT_LOCALE'] = 'es'  # Set Spanish as default locale
    app.config['BABEL_TRANSLATION_DIRECTORIES'] = '../translations'

    @app.context_processor
    def inject_locale():
        return dict(get_locale=get_locale)

    if config_override:
        app.config.update(config_override)

    db.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(main)
    app.register_blueprint(authorize)

    login_manager = LoginManager()
    login_manager.login_view = "authorize.login"
    login_manager.session_protection = "strong"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    return app

# Run the Flask app with the correct entry point
if __name__ == "__main__":
    app = create_app()
    app.run(ssl_context="adhoc", debug=True)
