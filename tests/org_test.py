"""Project: New Arrivals Chi.

File name: org_test.py

Associated Files: main.py, profile.html

This test suite performs more robust security testing for user authorization
routes and password handling mechanisms for the New Arrivals Chicago portal.

Methods:
   * test_create_organization_profile
   * test_organization_profile_page
   * test_create_post_new_org

Last updated:
@Author: Kathryn Link-Oberstar @klinkoberstar
@Date: 05/13/2024

Creation:
@Author: Kathryn Link-Oberstar @klinkoberstar
@Date: 05/12/2024
"""
from new_arrivals_chi.app.data_handler import create_organization_profile
from new_arrivals_chi.app.database import Organization


def test_create_organization_profile(client, setup_logger):
    """Test creating a new organization profile in the database."""
    logger = setup_logger("test_create_organization_profile")
    try:
        name = "New Org"
        phone = "987-654-3210"
        status = "ACTIVE"

        org_id = create_organization_profile(name, phone, status)
        assert org_id is not None, "Failed to create organization with valid data"

        created_org = Organization.query.get(org_id)
        assert created_org.name == name, "Organization name does not match the provided name"
        assert created_org.phone == phone, "Organization phone does not match the provided phone"
        assert created_org.status == status, "Organization status does not match the provided status"
        logger.info("Organization created successfully.")
    except AssertionError as e:
        logger.error(f"Test failed: {str(e)}")
        raise

def test_organization_profile_page(client, logged_in_state, capture_templates, test_user, setup_logger):
    """Test the organization profile page access and rendering."""
    logger = setup_logger("test_organization_profile_page")
    try:
        response = client.get("/profile")
        assert response.status_code == 200, "Failed to access the organization profile page"
        
        final_template_rendered = len(capture_templates) - 1
        assert (
            capture_templates[final_template_rendered][0].name == "profile.html"
        ), "Wrong template used"
        logger.info("Organization profile page rendered.")
    except AssertionError as e:
        logger.error(f"Test failed: {str(e)}")
        raise

def test_create_post_new_org(client, logged_in_state, capture_templates, setup_logger, test_user):
    """Tests creating a new organization."""
    logger = setup_logger("test_create_post_new_org")

    try:
        response = client.post(
            "/profile",
            data={
                "name": "New Org",  
                "phone": "987-654-3210",
                "status": "ACTIVE",
            },
            follow_redirects=True,
        )
        assert response.status_code == 200
        final_template_rendered = len(capture_templates) - 1
        assert (
            capture_templates[final_template_rendered][0].name == "profile.html"
        ), "Wrong template used"
        logger.info("Organization created and added to database successfully.")
    except AssertionError as e:
        logger.error(f"Test failed: {str(e)}")
        raise