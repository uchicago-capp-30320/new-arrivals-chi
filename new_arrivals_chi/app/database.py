from sqlalchemy import Enum, Table, ForeignKey, Column, Integer
from main import db

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


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    role = db.Column(
        Enum("admin", "standard", name="role_types"),
        nullable=False,
        default="standard",
    )
    password = db.Column(db.String(100), nullable=False)
    organization_id = db.Column(db.Integer, db.ForeignKey("organizations.id"))
    organization = db.relationship("Organization", back_populates="users")


class Organization(db.Model):
    __tablename__ = "organizations"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    location_id = db.Column(
        db.Integer, db.ForeignKey("locations.id"), nullable=False
    )
    hours_id = db.Column(db.Integer, db.ForeignKey("hours.id"), nullable=False)
    phone = db.Column(db.String(25), nullable=False)
    image_path = db.Column(db.String(255), nullable=True)
    status = db.Column(db.String(50), nullable=False)
    created_at = db.Column(
        db.DateTime, nullable=False, server_default=db.func.now()
    )
    deleted_at = db.Column(
        db.DateTime(timezone=True), nullable=True, server_default=None
    )
    created_by = db.Column(
        db.Integer, db.ForeignKey("users.id"), nullable=False
    )
    updated_by = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)

    # Relationships
    users = db.relationship("User", back_populates="organizations")
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
    locations = db.relationship("Location", back_populates="organizations")


class Language(db.Model):
    __tablename__ = "languages"
    id = db.Column(db.Integer, primary_key=True)
    language = db.Column(db.String(50), nullable=False)
    created_at = db.Column(
        db.DateTime(timezone=True), nullable=False, server_default=db.func.now()
    )
    deleted_at = db.Column(db.DateTime(timezone=True), nullable=True)
    created_by = db.Column(
        db.Integer, db.ForeignKey("users.id"), nullable=False
    )
    deleted_by = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    organizations = db.relationship(
        "Organization",
        secondary=languages_organizations,
        back_populates="languages",
    )


class Hours(db.Model):
    __tablename__ = "hours"
    id = db.Column(db.Integer, primary_key=True)
    day_of_week = db.Column(db.Integer, nullable=False)
    opening_time = db.Column(db.Time, nullable=False)
    closing_time = db.Column(db.Time, nullable=False)
    created_at = db.Column(
        db.DateTime(timezone=True), nullable=False, server_default=db.func.now()
    )
    deleted_at = db.Column(db.DateTime(timezone=True), nullable=True)
    created_by = db.Column(
        db.Integer, db.ForeignKey("users.id"), nullable=False
    )
    deleted_by = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    organizations = db.relationship(
        "Organization", secondary=organizations_hours, back_populates="hours"
    )


class Service(db.Model):
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
    created_by = db.Column(
        db.Integer, db.ForeignKey("users.id"), nullable=False
    )
    deleted_by = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    organizations = db.relationship(
        "Organization",
        secondary=organizations_services,
        back_populates="services",
    )
    locations = db.relationship(
        "Location", secondary=organizations_services, back_populates="services"
    )
    service_dates = db.relationship(
        "ServiceDate",
        secondary=service_dates_services,
        back_populates="services",
    )


class ServiceDate(db.Model):
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
    created_by = db.Column(
        db.Integer, db.ForeignKey("users.id"), nullable=False
    )
    deleted_by = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    service = db.relationship(
        "Service",
        secondary=service_dates_services,
        back_populates="service_dates",
    )


class Location(db.Model):
    __tablename__ = "locations"
    id = db.Column(db.Integer, primary_key=True)
    org_id = db.Column(
        db.Integer, db.ForeignKey("organizations.id"), nullable=False
    )
    street_address = db.Column(db.String(255), nullable=False)
    zip_code = db.Column(db.String(10), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(50), nullable=False)
    primary_location = db.Column(db.Integer, nullable=False)
    created_at = db.Column(
        db.DateTime(timezone=True), nullable=False, server_default=db.func.now()
    )
    deleted_at = db.Column(db.DateTime(timezone=True), nullable=True)
    created_by = db.Column(
        db.Integer, db.ForeignKey("users.id"), nullable=False
    )
    deleted_by = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    organizations = db.relationship("Organization", back_populates="locations")
