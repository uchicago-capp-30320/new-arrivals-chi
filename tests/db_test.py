from faker import Faker
from new_arrivals_chi.app.database import User, Organization, Location, Hours
from sqlalchemy.orm import Session
from sqlalchemy import select


fake = Faker()


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


def create_fake_data(num_users, database, logger):
    """
    Generate fake data for testing by creating multiple users
    and organizations with their locations and hours.

    Parameters:
    num_users (int): The number of users to create
    database (SQLAlchemy): The database object to interact with the database
    logger (Logger): The logger object to log messages

    Returns:
    None
    """
    logger.info("Starting to create fake data")
    try:
        for _ in range(num_users):
            org = create_fake_organization()
            database.session.add(org)

            initial_user = create_fake_user(org)
            database.session.add(initial_user)

            location = create_fake_location(initial_user.id)
            database.session.add(location)

            hours = create_fake_hours(initial_user.id)
            database.session.add(hours)

        database.session.commit()
        logger.info(
            f"Added org, user, location & hours for user {initial_user.id}"
        )
    except Exception as e:
        database.session.rollback()
        logger.error(f"Error creating data: {e}, rolling back changes")
    else:
        logger.info("Fake data creation completed successfully")


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


def test_user_organization_creation(app, setup_logger, database):
    """
    Test creating users and organizations and retrieving them.
    Uses the 'app' fixture for application context, 'setup_logger' for logging,
    and 'database' for interacting with the database.
    """
    logger = setup_logger("test_user_organization_creation")

    with app.app_context():
        logger.info("Starting test by creating fake data")
        create_fake_data(
            5, database, logger
        )  # Pass the database and logger to the function
        logger.info("Fake data created")

        with Session(bind=database.engine) as session:
            logger.info("Attempting to retrieve user with ID 1")
            user = session.get(User, 1)
            assert user is not None, "No user found with ID 1"
            assert "@" in user.email, "User email format is incorrect"
            assert user.role in [
                "admin",
                "standard",
            ], "User role is not set correctly"
            logger.info("User retrieved and validated successfully")

            logger.info(
                "Retrieving all users to validate total count and links"
            )
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
            logger.info("All users retrieved and validated successfully")
