"""Project: New Arrivals Chi.

File name: org_test.py

Associated Files: main.py, dashboard.html

This test suite performs more robust security testing for user authorization
routes and password handling mechanisms for the New Arrivals Chicago portal.

Methods:
   * test_create_organization_dashboard
   * test_organization_dashboard_page
   * test_create_post_new_org
"""

from new_arrivals_chi.app.database import Organization
from new_arrivals_chi.app.data_handler import create_organization_profile
from http import HTTPStatus

def test_create_organization_dashboard(client, setup_logger):
    """Test creating a new organization dashboard in the database."""
    logger = setup_logger("test_create_organization_dashboard")
    try:
        name = "New Org"
        phone = "987-654-3210"
        status = "ACTIVE"

        org_id = create_organization_profile(name, phone, status)
        assert (
            org_id is not None
        ), "Failed to create organization with valid data"

        created_org = Organization.query.get(org_id)
        assert (
            created_org.name == name
        ), "Organization name does not match the provided name"
        assert (
            created_org.phone == phone
        ), "Organization phone does not match the provided phone"
        assert (
            created_org.status == status
        ), "Organization status does not match the provided status"
        logger.info("Organization created successfully.")
    except AssertionError as e:
        logger.error(f"Test failed: {str(e)}")
        raise


def test_organization_dashboard_page(
    client, logged_in_state, capture_templates, test_user, setup_logger
):
    """Test the organization dashboard page access and rendering."""
    logger = setup_logger("test_organization_dashboard_page")
    try:
        response = client.get("/dashboard")
        assert (
            response.status_code == HTTPStatus.OK
        ), "Failed to access the organization dashboard page"

        final_template_rendered = len(capture_templates) - 1
        assert (
            capture_templates[final_template_rendered][0].name
            == "dashboard.html"
        ), "Wrong template used"
        logger.info("Organization dashboard page rendered.")
    except AssertionError as e:
        logger.error(f"Test failed: {str(e)}")
        raise
