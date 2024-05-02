import pytest
from faker import Faker
from new_arrivals_chi.app.main import db, create_app
from new_arrivals_chi.app.database import User, Organization, Location, Hours
from new_arrivals_chi.app.logger_config import setup_logger
from sqlalchemy.orm import Session
from sqlalchemy import select


fake = Faker()
test_logger = setup_logger("test")


def create_fake_location(user_id):
    """Create a single fake location instance that requires a user."""
    return Location(
        street_address=fake.street_address(),
        zip_code=fake.zipcode(),
        city=fake.city(),
        state=fake.state(),
        primary_location=fake.boolean(),
        created_by=user_id,
    )


def create_fake_hours(user_id):
    """Create a single fake hours instance"""
    return Hours(
        day_of_week=fake.random_int(min=0, max=6),  # 0-6 for Sunday to Saturday
        opening_time=fake.time_object(),
        closing_time=fake.time_object(),
        created_by=user_id,
    )


def create_fake_organization():
    """Create a single fake organization instance."""
    return Organization(
        name=fake.company(),
        phone=fake.phone_number(),
        image_path=fake.image_url(),
        status=fake.random_element(elements=("ACTIVE", "SUSPENDED", "HIDDEN")),
    )


def create_fake_user(organization):
    """Create a single fake user instance associated with an organization."""
    return User(
        email=fake.email(),
        role=fake.random_element(elements=("admin", "standard")),
        password=fake.password(),
        organization=organization,
    )


def create_fake_data(num_users=1):
    """Generate fake data for testing by creating multiple users
    and organizations along with their locations."""
    try:
        db.create_all()

        for _ in range(num_users):
            org = create_fake_organization()
            db.session.add(org)
            db.session.commit()

            initial_user = create_fake_user(org)
            db.session.add(initial_user)

            location = create_fake_location(initial_user.id)
            db.session.add(location)

            hours = create_fake_hours(initial_user.id)
            db.session.add(hours)
            db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(f"Error creating data: {e}")


def get_record_by_id(model, record_id):
    """Retrieve a single record by its ID."""
    return model.query.get(record_id)


def get_record_by_attribute(model, **kwargs):
    """Retrieve a single record by a specified attribute."""
    return model.query.filter_by(**kwargs).first()


def fetch_data():
    """Fetch and print data from the database to verify insertion."""
    users = User.query.all()
    for user in users:
        print(f"User: {user.email}, Organization: {user.organization.name}")


@pytest.mark.usefixtures("app")
def test_user_organization_creation(app):
    """Test creating users and organizations and retrieving them."""
    app = create_app()
    with app.app_context():
        db.drop_all()
        db.create_all()
        create_fake_data(5)

        with Session(bind=db.engine) as session:
            # Retrieve user by primary key
            user = session.get(User, 1)
            assert user is not None, "No user found with ID 1"
            assert "@" in user.email, "User email format is incorrect"
            assert user.role in [
                "admin",
                "standard",
            ], "User role is not set correctly"

            # Retrieve organization by name using select
            org_select = select(Organization).where(
                Organization.name == user.organization.name
            )
            organization = session.execute(org_select).scalar_one_or_none()
            assert (
                organization is not None
            ), "No organization found with specified name"
            assert organization.status in [
                "ACTIVE",
                "SUSPENDED",
                "HIDDEN",
            ], "Organization status is incorrect"

            # Retrieve all users using select
            users_select = select(User)
            users = session.execute(users_select).scalars().all()
            assert (
                len(users) == 5
            ), "Number of users created and retrieved does not match"
            for user in users:
                assert (
                    user.organization is not None
                ), "User organization is not linked properly"
                assert (
                    user.organization.phone
                ), "Organization phone number is missing"
