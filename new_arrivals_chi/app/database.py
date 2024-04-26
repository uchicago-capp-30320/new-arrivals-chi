from sqlalchemy import Enum
from main import db


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100), nullable=False)
    organization_id = db.Column(
        db.Integer, db.ForeignKey("organization.id"), nullable=True
    )
    organization = db.relationship("Organization", back_populates="users")


languages_organizations = db.Table(
    "languages_organizations",
    db.Column(
        "language_id",
        db.Integer,
        db.ForeignKey("language.id"),
        primary_key=True,
    ),
    db.Column(
        "organization_id",
        db.Integer,
        db.ForeignKey("organization.id"),
        primary_key=True,
    ),
)

services_organizations = db.Table(
    "services_organizations",
    db.Column(
        "service_id", db.Integer, db.ForeignKey("service.id"), primary_key=True
    ),
    db.Column(
        "organization_id",
        db.Integer,
        db.ForeignKey("organization.id"),
        primary_key=True,
    ),
)


class Organization(db.Model):
    __tablename__ = "organizations"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    location_id = db.Column(
        db.Integer, db.ForeignKey("location.id"), nullable=False
    )
    hours_id = db.Column(db.Integer, db.ForeignKey("hours.id"), nullable=False)
    phone = db.Column(db.String(25), nullable=False)
    image_path = db.Column(db.String(255), nullable=True)
    status = db.Column(db.String(50), nullable=False)
    users = db.relationship("User", back_populates="organizations")
    languages = db.relationship(
        "Language",
        secondary=languages_organizations,
        back_populates="organizations",
    )
    services = db.relationship(
        "Service",
        secondary=services_organizations,
        back_populates="organizations",
    )


class Language(db.Model):
    __tablename__ = "languages"
    id = db.Column(db.Integer, primary_key=True)
    org_id = db.Column(
        db.Integer, db.ForeignKey("organization.id"), nullable=False
    )
    language = db.Column(db.String(50), nullable=False)
    organizations = db.relationship(
        "Organization",
        secondary=languages_organizations,
        back_populates="languages",
    )


class Hours(db.Model):
    __tablename__ = "hours"
    id = db.Column(db.Integer, primary_key=True)
    org_id = db.Column(
        db.Integer, db.ForeignKey("organization.id"), nullable=False
    )
    day_of_week = db.Column(db.Integer, nullable=False)
    opening_time = db.Column(db.Time, nullable=False)
    closing_time = db.Column(db.Time, nullable=False)


class Services(db.Model):
    __tablename__ = "services"
    id = db.Column(db.Integer, primary_key=True)
    org_id = db.Column(
        db.Integer, db.ForeignKey("organization.id"), nullable=False
    )
    location_id = db.Column(
        db.Integer, db.ForeignKey("location.id"), nullable=False
    )
    date_id = db.Column(db.Integer, db.ForeignKey("date.id"), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    service = db.Column(db.String(100), nullable=False)
    access = db.Column(db.String(100), nullable=False)
    service_note = db.Column(db.String(255), nullable=True)
    organizations = db.relationship(
        "Organization",
        secondary=services_organizations,
        back_populates="services",
    )


class ServiceDate(db.Model):
    __tablename__ = "service_dates"
    id = db.Column(db.Integer, primary_key=True)
    org_id = db.Column(
        db.Integer, db.ForeignKey("organization.id"), nullable=False
    )
    service_id = db.Column(
        db.Integer, db.ForeignKey("services.id"), nullable=False
    )
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
    __tablename__ = "locations"
    id = db.Column(db.Integer, primary_key=True)
    org_id = db.Column(
        db.Integer, db.ForeignKey("organization.id"), nullable=False
    )
    street_address = db.Column(db.String(255), nullable=False)
    zip_code = db.Column(db.String(10), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(50), nullable=False)
    primary_location = db.Column(db.Integer, nullable=False)
