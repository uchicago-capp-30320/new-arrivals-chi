from flask import Flask, Blueprint, render_template, request
import os
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


main = Blueprint("main", __name__)


load_dotenv()


@main.route("/")
def home():
    language = request.args.get("lang", "en")
    return render_template("home.html", language=language)


@main.route("/legal")
def legal():
    language = request.args.get("lang", "en")
    return render_template("legal.html", language=language)


app = Flask(__name__)
app.register_blueprint(main)

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)


if __name__ == "__main__":
    app.run(debug=True)
