"""
Script with the corresponding models for the database.
"""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Organization(db.model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    location_id = db.Column(
        db.Integer, db.ForeignKey("location.id"), nullable=False
    )
    hours_id = db.Column(db.Integer, db.ForeignKey("hours.id"), nullable=False)
    phone = db.Column(db.String, nullable=False)
    image_path = db.Column(db.String, nullable=False)
    status = db.Column(db.String, nullable=False)
