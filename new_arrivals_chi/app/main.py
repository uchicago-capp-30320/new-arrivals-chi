from flask import Flask, Blueprint, render_template, request

main = Blueprint("main", __name__)


@main.route("/")
def home():
    language = request.args.get("lang", "en")
    return render_template("home.html", language=language)


@main.route("/legal")
def legal():
    language = request.args.get("lang", "en")
    return render_template("legal.html", language=language)


# @auth.route('/signup')
@main.route("/signup")
def signup():
    """
    Establishes route for the user sign up page. This route is accessible
    within the 'sign up' button in the navigation bar.

    Returns:
        Renders sign up page in their selected language.
    """

    language = request.args.get("lang", "en")
    return render_template("signup.html", language=language)


app = Flask(__name__)

app.register_blueprint(main)

if __name__ == "__main__":
    app.run(debug=True)
