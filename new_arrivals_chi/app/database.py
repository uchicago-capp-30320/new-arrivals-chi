"""This script contains the corresponding database models for the app."""

from sqlalchemy import Enum, Table, ForeignKey, Column, Integer
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

# Association Tables for Many-to-Many relationships
languages_organizations = Table(
    "languages_organizations",
    db.Model.metadata,
    Column(
        "language_id", Integer, ForeignKey("languages.id"), primary_key=True
    ),
    Column(
        "organization_id",
        Integer,
        ForeignKey("organizations.id"),
        primary_key=True,
    ),
)

organizations_hours = Table(
    "organizations_hours",
    db.Model.metadata,
    Column("hours_id", Integer, ForeignKey("hours.id"), primary_key=True),
    Column(
        "organization_id",
        Integer,
        ForeignKey("organizations.id"),
        primary_key=True,
    ),
)

organizations_services = Table(
    "organizations_services",
    db.Model.metadata,
    Column("service_id", Integer, ForeignKey("services.id"), primary_key=True),
    Column(
        "organization_id",
        Integer,
        ForeignKey("organizations.id"),
        primary_key=True,
    ),
)

# Association Table for Services and Service Dates
service_dates_services = db.Table(
    "service_dates_services",
    db.Model.metadata,
    db.Column(
        "service_id", db.Integer, db.ForeignKey("services.id"), primary_key=True
    ),
    db.Column(
        "service_date_id",
        db.Integer,
        db.ForeignKey("service_dates.id"),
        primary_key=True,
    ),
)

location_services = db.Table(
    "location_services",
    db.Model.metadata,
    db.Column(
        "location_id",
        db.Integer,
        db.ForeignKey("locations.id"),
        primary_key=True,
    ),
    db.Column(
        "service_id",
        db.Integer,
        db.ForeignKey("services.id"),
        primary_key=True,
    ),
)


class User(UserMixin, db.Model):
    """Class for the users table in the database."""

    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    role = db.Column(
        Enum("admin", "standard", name="role_types"),
        nullable=False,
        default="standard",
    )
    password = db.Column(db.String(255), nullable=False)
    organization_id = db.Column(
        db.Integer,
        db.ForeignKey("organizations.id", name="users_organization_id_fkey"),
        nullable=True,
    )
    organization = db.relationship(
        "Organization", back_populates="users", foreign_keys=[organization_id]
    )


class Organization(db.Model):
    """Class for the organizations table in the database."""

    __tablename__ = "organizations"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(260), nullable=False)
    location_id = db.Column(
        db.Integer,
        db.ForeignKey("locations.id", name="organizations_location_id_fkey"),
        nullable=True,
    )
    hours_id = db.Column(
        db.Integer,
        db.ForeignKey("hours.id", name="organizations_hours_id_fkey"),
        nullable=True,
    )
    phone = db.Column(db.String(25), nullable=False)
    image_path = db.Column(db.String(255), nullable=True)
    status = db.Column(db.String(50), nullable=False)
    created_at = db.Column(
        db.DateTime, nullable=False, server_default=db.func.now()
    )
    deleted_at = db.Column(
        db.DateTime(timezone=True), nullable=True, server_default=None
    )
    created_by = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    updated_by = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)

    # Relationships
    users = db.relationship(
        "User",
        back_populates="organization",
        foreign_keys="User.organization_id",
    )
    languages = db.relationship(
        "Language",
        secondary=languages_organizations,
        back_populates="organizations",
    )
    services = db.relationship(
        "Service",
        secondary=organizations_services,
        back_populates="organizations",
    )
    hours = db.relationship(
        "Hours", secondary=organizations_hours, back_populates="organizations"
    )
    locations = db.relationship("Location", back_populates="organization")


class Language(db.Model):
    """Class for the languages table in the database."""

    __tablename__ = "languages"
    id = db.Column(db.Integer, primary_key=True)
    language = db.Column(db.String(50), nullable=False)
    created_at = db.Column(
        db.DateTime(timezone=True), nullable=False, server_default=db.func.now()
    )
    deleted_at = db.Column(db.DateTime(timezone=True), nullable=True)
    created_by = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    deleted_by = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    organizations = db.relationship(
        "Organization",
        secondary=languages_organizations,
        back_populates="languages",
    )


class Hours(db.Model):
    """Class for the hours table in the database."""

    __tablename__ = "hours"
    id = db.Column(db.Integer, primary_key=True)
    day_of_week = db.Column(db.Integer, nullable=False)
    opening_time = db.Column(db.Time, nullable=False)
    closing_time = db.Column(db.Time, nullable=False)
    created_at = db.Column(
        db.DateTime(timezone=True), nullable=False, server_default=db.func.now()
    )
    deleted_at = db.Column(db.DateTime(timezone=True), nullable=True)
    created_by = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    deleted_by = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    organizations = db.relationship(
        "Organization", secondary=organizations_hours, back_populates="hours"
    )


class Service(db.Model):
    """Class for the services table in the database."""

    __tablename__ = "services"
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(100), nullable=False)
    service = db.Column(db.String(100), nullable=False)
    access = db.Column(db.String(100), nullable=False)
    service_note = db.Column(db.String(255), nullable=True)
    created_at = db.Column(
        db.DateTime(timezone=True), nullable=False, server_default=db.func.now()
    )
    deleted_at = db.Column(db.DateTime(timezone=True), nullable=True)
    created_by = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    deleted_by = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    organizations = db.relationship(
        "Organization",
        secondary=organizations_services,
        back_populates="services",
    )
    locations = db.relationship(
        "Location", secondary=location_services, back_populates="services"
    )
    service_dates = db.relationship(
        "ServiceDate",
        secondary=service_dates_services,
        back_populates="services",
    )


class ServiceDate(db.Model):
    """Class for the service_dates table in the database."""

    __tablename__ = "service_dates"
    id = db.Column(db.Integer, primary_key=True)
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
    created_at = db.Column(
        db.DateTime(timezone=True), nullable=False, server_default=db.func.now()
    )
    deleted_at = db.Column(db.DateTime(timezone=True), nullable=True)
    created_by = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    deleted_by = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    services = db.relationship(
        "Service",
        secondary=service_dates_services,
        back_populates="service_dates",
    )


class Location(db.Model):
    """Class for the locations table in the database."""

    __tablename__ = "locations"
    id = db.Column(db.Integer, primary_key=True)
    street_address = db.Column(db.String(255), nullable=False)
    zip_code = db.Column(db.String(10), nullable=False)
    neighborhood = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(50), nullable=False)
    primary_location = db.Column(db.Boolean, nullable=False)
    created_at = db.Column(
        db.DateTime(timezone=True), nullable=False, server_default=db.func.now()
    )
    deleted_at = db.Column(db.DateTime(timezone=True), nullable=True)
    created_by = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    deleted_by = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    organization = db.relationship("Organization", back_populates="locations")
    services = db.relationship(
        "Service", secondary=location_services, back_populates="locations"
    )
