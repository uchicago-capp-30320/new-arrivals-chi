from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Enum
from app import db


class Organization(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    location_id = db.Column(db.Integer, db.ForeignKey("location.id"), nullable=False)
    hours_id = db.Column(db.Integer, db.ForeignKey("hours.id"), nullable=False)
    phone = db.Column(db.String(25), nullable=False)
    image_path = db.Column(db.String(255), nullable=False)
    status = db.Column(db.String(50), nullable=False)


class Language(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    org_id = db.Column(db.Integer, db.ForeignKey("organization.id"), nullable=False)
    language = db.Column(db.String(50), nullable=False)


class Hours(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    org_id = db.Column(db.Integer, db.ForeignKey("organization.id"), nullable=False)
    day_of_week = db.Column(db.Integer, nullable=False)
    opening_time = db.Column(db.Time, nullable=False)
    closing_time = db.Column(db.Time, nullable=False)


class Services(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    org_id = db.Column(db.Integer, db.ForeignKey("organization.id"), nullable=False)
    location_id = db.Column(db.Integer, db.ForeignKey("location.id"), nullable=False)
    date_id = db.Column(db.Integer, db.ForeignKey("date.id"), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    service = db.Column(db.String(100), nullable=False)
    access = db.Column(db.String(100), nullable=False)
    service_note = db.Column(db.String(255), nullable=True)


class ServiceDate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    org_id = db.Column(db.Integer, db.ForeignKey("organization.id"), nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey("services.id"), nullable=False)
    date = db.Column(db.Date, nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    repeat = db.Column(
        Enum(
            "every day",
            "every week",
            "every month",
            "every other week",
            name="repeat_types",
        ),
        nullable=False,
    )


class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    org_id = db.Column(db.Integer, db.ForeignKey("organization.id"), nullable=False)
    street_address = db.Column(db.String(255), nullable=False)
    zip_code = db.Column(db.String(10), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(50), nullable=False)
    primary_location = db.Column(db.Integer, nullable=False)
