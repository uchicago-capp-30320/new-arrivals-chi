# will change to auth.route when the database is usable
from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from database import db, User
from flask_login import login_user, login_required, logout_user, current_user
import re
from utils import validate_email_syntax, validate_password

authorize = Blueprint("authorize", __name__, static_folder="/static")

@authorize.route("/login")
def login():
    """
    Establishes route for the login page. This route is accessible
    within the 'login' button in the navigation bar.

    Returns:
        Renders login page for user with their selected language.
    """

    language = request.args.get("lang", "en")
    return render_template("login.html", language=language)



@authorize.route("/signup")
def signup():
    """
    Establishes route for the user sign up page. This route is accessible
    within the 'sign up' button in the navigation bar.

    Returns:
        Renders sign up page in their selected language.
    """

    language = request.args.get("lang", "en")
    return render_template("signup.html", language=language)

@authorize.route('/signup', methods=['POST'])
def signup_post():
    # code to validate and add user to database goes here
    email = request.form.get('email')
    password = request.form.get('password')

    # sanitize input

    # ensure that input meets requirments
    email_synax = validate_email_syntax(email)

    if not email_synax:
        flash('Please enter a valid email address')
        return redirect(url_for('authorize.signup'))

    # password: 8+ characters, 1+ number, 1+ special characters, not commonly used password, cannot be empty, cannot contain certain special chars, no spaces
    password_strength = validate_password(password)
    
    if not password_strength:
        flash('Please enter a valid password')
        return redirect(url_for('authorize.signup'))
    
    user = User.query.filter_by(email=email).first() #if this returns a user, then the email already exists in database
    #print(user)
    if user: # if a user is found, we want to redirect back to signup page so user can try again
        flash('Email address already exists')
        return redirect(url_for('authorize.signup'))
   
    # normalize password before hashing?

    # create a new user with the form data. Hash the password so the plaintext version isn't saved.
    # Salt ?
    new_user = User(email=email, password=generate_password_hash(password, method='pbkdf2:sha256'))
    #new_user = User(email=email, password=password)
    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()

    #return redirect(url_for('auth.login'))
    return redirect(url_for('main.home'))