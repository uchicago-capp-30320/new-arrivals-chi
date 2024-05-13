# org_test.py
from new_arrivals_chi.app.data_handler import create_organization_profile
from new_arrivals_chi.app.database import Organization, User


def test_create_organization_profile(client):
    """Test creating a new organization profile in the database."""
    name = "New Org"
    phone = "987-654-3210"
    status = "ACTIVE"

    org_id = create_organization_profile(name, phone, status)
    assert org_id is not None, "Failed to create organization with valid data"

    created_org = Organization.query.get(org_id)
    assert created_org.name == name, "Organization name does not match the provided name"
    assert created_org.phone == phone, "Organization phone does not match the provided phone"
    assert created_org.status == status, "Organization status does not match the provided status"

def test_organization_profile_page(client, logged_in_state, capture_templates, test_user):
    """Test the organization profile page access and rendering."""
    response = client.get("/profile")
    assert response.status_code == 200, "Failed to access the organization profile page"
    
    final_template_rendered = len(capture_templates) - 1
    assert (
        capture_templates[final_template_rendered][0].name == "profile.html"
    ), "Wrong template used"

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