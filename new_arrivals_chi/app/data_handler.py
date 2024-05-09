from werkzeug.security import generate_password_hash
from new_arrivals_chi.app.database import db, User
from flask_login import login_user, login_required, logout_user, current_user

def create_user(email, password):
    new_user = User(
        email=email,
        password=generate_password_hash(password, method="pbkdf2:sha256"),
    )
    db.session.add(new_user)
    db.session.commit()

    return new_user

def change_db_password(password):
    current_user.password = generate_password_hash(
        password, method="pbkdf2:sha256"
    )
    db.session.commit()
