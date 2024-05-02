"""
Project: new_arrivals_chi
File name: main.py
Associated Files:
    Templates: base.html, home.html, legal.html, profile.html,
    login.html, info.html

Runs primary flask application for Chicago's new arrivals' portal.

Methods:
    * home — Route to homepage of application.
    * profile - Route to user's profile.
    * legal - Route to legal portion of application.

Last updated:
@Author: Madeleine Roberts @MadeleineKRoberts
@Date: 04/25/2024

Creation:
@Author: Summer Long @Sumslong
@Date: 04/19/2024
"""

from flask import Flask, Blueprint, render_template, request
import os
from dotenv import load_dotenv
from new_arrivals_chi.app.authorize_routes import authorize
from new_arrivals_chi.app.database import db
from flask_migrate import Migrate

migrate = Migrate()

load_dotenv()

main = Blueprint("main", __name__, static_folder="/static")


@main.route("/")
def home():
    """
    Establishes route for the home page of New Arrivals Chi. This route is
    accessible within the 'home' button in the navigation bar and is the page
    that users are directed to when first visiting the site.

    Returns:
        Renders home page.
    """

    language = request.args.get("lang", "en")
    return render_template("home.html", language=language)


@main.route("/profile")
def profile():
    """
    Establishes route for the user's profile page. This route is accessible
    within the 'profile' button in the navigation bar.

    Returns:
        Renders profile page for user with in their selected language.
    """

    language = request.args.get("lang", "en")
    return render_template("profile.html", language=language)


@main.route("/legal")
def legal():
    """
    Establishes route for the legal page. This route is accessible
    within the 'legal' button in the navigation bar.

    Returns:
        Renders main legal page.
    """

    language = request.args.get("lang", "en")
    return render_template("legal.html", language=language)


@main.route("/info")
def info():
    """
    Establishes route for an unauthenticated view of an organization's
    information. This will be accessible when search is implemented.

    Returns:
        Renders information of an organization.
    """

    language = request.args.get("lang", "en")
    return render_template("info.html", language=language)


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
        "DATABASE_URL", default="sqlite:///:memory:"
    )
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(main)
    app.register_blueprint(authorize)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
