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


class Language(db.model):
    id = db.Column(db.Integer, primary_key=True)
    org_id = db.Column(
        db.Integer, db.ForeignKey("organization.id"), nullable=False
    )
    language = db.Column(db.String, nullable=False)


class Hours:
    id = db.Column(db.Integer, primary_key=True)
    org_id = db.Column(
        db.Integer, db.ForeignKey("organization.id"), nullable=False
    )
    day_of_week = db.Column(db.Integer, nullable=False)
    opening_time = db.Column(db.Time, nullable=False)
    closing_time = db.Column(db.Time, nullable=False)


class Services:
    id = db.Column(db.Integer, primary_key=True)
    org_id = db.Column(
        db.Integer, db.ForeignKey("organization.id"), nullable=False
    )
    location_id = db.Column(
        db.Integer, db.ForeignKey("location.id"), nullable=False
    )
    date_id = db.Column(db.Integer, db.ForeignKey("date.id"), nullable=False)
    category = db.Column(db.String, nullable=False)
    service = db.Column(db.String, nullable=False)
    access = db.Column(db.String, nullable=False)
    service_note = db.Column(db.String, nullable=True)


class ServiceDate:
    id = db.Column(db.Integer, primary_key=True)
    org_id = db.Column(
        db.Integer, db.ForeignKey("organization.id"), nullable=False
    )
    service_id = db.Column(
        db.Integer, db.ForeignKey("service.id"), nullable=False
    )
    date = db.Column(db.Date, nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    repeat = db.Column(db.Enum, nullable=False)


class Location:
    id = db.Column(db.Integer, primary_key=True)
    org_id = db.Column(
        db.Integer, db.ForeignKey("organization.id"), nullable=False
    )
    street_address = db.Column(db.String, nullable=False)
    zip_code = db.Column(db.String, nullable=False)
    city = db.Column(db.String, nullable=False)
    state = db.Column(db.String, nullable=False)
    primary_location = db.Column(db.Integer, nullable=False)
