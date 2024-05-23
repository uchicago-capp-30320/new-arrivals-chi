"""Project: New Arrivals Chi.

File name: legal_routes_test.py

Associated Files:
    Templates: legal.html, tps_info.html, tps_apply.html, vttc_info.html,
    vttc_apply.html, asylum_info.html, asylum_apply.html, parole_info.html,
    parole_apply.html, undocumented_resources.html, help.html,
    work_rights.html, renters_rights.html, general.html.

This test suite verifies the functionality of the legal routes,
including testing various scenarios such as accessing legal pages
and ensuring the correct templates are rendered.

Methods:
    * test_access_legal_page
    * test_access_legal_route
"""

from http import HTTPStatus
import pytest

@pytest.mark.parametrize(
    "route, template",
    [
        ("/legal", "legal_flow.html"),
        ("/legal/tps_info", "tps_info.html"),
        ("/legal/tps_apply", "tps_apply.html"),
        ("/legal/vttc_info", "vttc_info.html"),
        ("/legal/vttc_apply", "vttc_apply.html"),
        ("/legal/asylum_info", "asylum_info.html"),
        ("/legal/asylum_apply", "asylum_apply.html"),
        ("/legal/parole_info", "parole_info.html"),
        ("/legal/parole_apply", "parole_apply.html"),
        ("/legal/undocumented_resources", "undocumented_resources.html"),
        ("/legal/lawyers", "lawyers.html"),
        ("/legal/work_rights", "work_rights.html"),
        ("/legal/renters_rights", "renters_rights.html"),
    ]
)
def test_access_legal_route(client, capture_templates, setup_logger, route, template):
    """Test access to various legal routes and verifies the correct template is rendered.

    Args:
        client: The test client used for making requests.
        capture_templates: Context manager to capture templates rendered.
        setup_logger: Setup logger.
        route: The route to access.
        template: The expected template to be rendered.
    """
    logger = setup_logger(f"test_access_{route.strip('/').replace('/', '_')}")
    try:
        response = client.get(route, follow_redirects=True)
        assert response.status_code == HTTPStatus.OK
        final_template_rendered = len(capture_templates) - 1
        assert (
            capture_templates[final_template_rendered][0].name == template
        ), f"Wrong template used for route {route}"
        logger.info(f"{route} page rendered correctly.")
    except AssertionError as e:
        logger.error(f"Test failed for {route}: {str(e)}")
        raise


def test_access_legal_page(client, capture_templates, setup_logger):
    """Test Access Legal Page.

    Verifies that the legal page is accessible.
    Ensures that the correct template is rendered when accessing this page.

    Args:
        client: The test client used for making requests.
        capture_templates: Context manager to capture templates rendered.
        setup_logger: Setup logger.
    """
    logger = setup_logger("test_access_legal_page")
    try:
        response = client.get("/legal", follow_redirects=True)
        assert response.status_code == HTTPStatus.OK
        final_template_rendered = len(capture_templates) - 1
        assert (
            capture_templates[final_template_rendered][0].name
            == "legal_flow.html"
        )
        logger.info("Legal page rendered correctly.")
    except AssertionError as e:
        logger.error(f"Test failed: {str(e)}")
        raise
