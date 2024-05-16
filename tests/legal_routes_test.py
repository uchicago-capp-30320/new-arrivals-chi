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
    * test_access_legal_tps_info
    * test_access_legal_tps_apply
    * test_access_legal_vttc_info
    * test_access_legal_vttc_apply
    * test_access_legal_asylum_info
    * test_access_legal_asylum_apply
    * test_access_legal_parole_info
    * test_access_legal_parole_apply
    * test_access_legal_undocumented_resources
    * test_access_legal_help
    * test_access_legal_work_rights
    * test_access_legal_renters_rights
    * test_access_legal_general
"""
from http import HTTPStatus


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


def test_access_legal_tps_info(client, capture_templates, setup_logger):
    """Test Access TPS Info Page."""
    logger = setup_logger("test_access_legal_tps_info")
    try:
        response = client.get("/legal/tps_info", follow_redirects=True)
        assert response.status_code == HTTPStatus.OK
        final_template_rendered = len(capture_templates) - 1
        assert (
            capture_templates[final_template_rendered][0].name
            == "tps_info.html"
        )
        logger.info("TPS Info page rendered correctly.")
    except AssertionError as e:
        logger.error(f"Test failed: {str(e)}")
        raise


def test_access_legal_tps_apply(client, capture_templates, setup_logger):
    """Test Access TPS Apply Page."""
    logger = setup_logger("test_access_legal_tps_apply")
    try:
        response = client.get("/legal/tps_apply", follow_redirects=True)
        assert response.status_code == HTTPStatus.OK
        final_template_rendered = len(capture_templates) - 1
        assert (
            capture_templates[final_template_rendered][0].name
            == "tps_apply.html"
        )
        logger.info("TPS Apply page rendered correctly.")
    except AssertionError as e:
        logger.error(f"Test failed: {str(e)}")
        raise


def test_access_legal_vttc_info(client, capture_templates, setup_logger):
    """Test Access VTTC Info Page."""
    logger = setup_logger("test_access_legal_vttc_info")
    try:
        response = client.get("/legal/vttc_info", follow_redirects=True)
        assert response.status_code == HTTPStatus.OK
        final_template_rendered = len(capture_templates) - 1
        assert (
            capture_templates[final_template_rendered][0].name
            == "vttc_info.html"
        )
        logger.info("VTTC Info page rendered correctly.")
    except AssertionError as e:
        logger.error(f"Test failed: {str(e)}")
        raise


def test_access_legal_vttc_apply(client, capture_templates, setup_logger):
    """Test Access VTTC Apply Page."""
    logger = setup_logger("test_access_legal_vttc_apply")
    try:
        response = client.get("/legal/vttc_apply", follow_redirects=True)
        assert response.status_code == HTTPStatus.OK
        final_template_rendered = len(capture_templates) - 1
        assert (
            capture_templates[final_template_rendered][0].name
            == "vttc_apply.html"
        )
        logger.info("VTTC Apply page rendered correctly.")
    except AssertionError as e:
        logger.error(f"Test failed: {str(e)}")
        raise


def test_access_legal_asylum_info(client, capture_templates, setup_logger):
    """Test Access Asylum Info Page."""
    logger = setup_logger("test_access_legal_asylum_info")
    try:
        response = client.get("/legal/asylum_info", follow_redirects=True)
        assert response.status_code == HTTPStatus.OK
        final_template_rendered = len(capture_templates) - 1
        assert (
            capture_templates[final_template_rendered][0].name
            == "asylum_info.html"
        )
        logger.info("Asylum Info page rendered correctly.")
    except AssertionError as e:
        logger.error(f"Test failed: {str(e)}")
        raise


def test_access_legal_asylum_apply(client, capture_templates, setup_logger):
    """Test Access Asylum Apply Page."""
    logger = setup_logger("test_access_legal_asylum_apply")
    try:
        response = client.get("/legal/asylum_apply", follow_redirects=True)
        assert response.status_code == HTTPStatus.OK
        final_template_rendered = len(capture_templates) - 1
        assert (
            capture_templates[final_template_rendered][0].name
            == "asylum_apply.html"
        )
        logger.info("Asylum Apply page rendered correctly.")
    except AssertionError as e:
        logger.error(f"Test failed: {str(e)}")
        raise


def test_access_legal_parole_info(client, capture_templates, setup_logger):
    """Test Access Parole Info Page."""
    logger = setup_logger("test_access_legal_parole_info")
    try:
        response = client.get("/legal/parole_info", follow_redirects=True)
        assert response.status_code == HTTPStatus.OK
        final_template_rendered = len(capture_templates) - 1
        assert (
            capture_templates[final_template_rendered][0].name
            == "parole_info.html"
        )
        logger.info("Parole Info page rendered correctly.")
    except AssertionError as e:
        logger.error(f"Test failed: {str(e)}")
        raise


def test_access_legal_parole_apply(client, capture_templates, setup_logger):
    """Test Access Parole Apply Page."""
    logger = setup_logger("test_access_legal_parole_apply")
    try:
        response = client.get("/legal/parole_apply", follow_redirects=True)
        assert response.status_code == HTTPStatus.OK
        final_template_rendered = len(capture_templates) - 1
        assert (
            capture_templates[final_template_rendered][0].name
            == "parole_apply.html"
        )
        logger.info("Parole Apply page rendered correctly.")
    except AssertionError as e:
        logger.error(f"Test failed: {str(e)}")
        raise


def test_access_legal_undocumented_resources(
    client, capture_templates, setup_logger
):
    """Test Access Undocumented Resources Page."""
    logger = setup_logger("test_access_legal_undocumented_resources")
    try:
        response = client.get(
            "/legal/undocumented_resources", follow_redirects=True
        )
        assert response.status_code == HTTPStatus.OK
        final_template_rendered = len(capture_templates) - 1
        assert (
            capture_templates[final_template_rendered][0].name
            == "undocumented_resources.html"
        )
        logger.info("Undocumented Resources page rendered correctly.")
    except AssertionError as e:
        logger.error(f"Test failed: {str(e)}")
        raise


def test_access_legal_help(client, capture_templates, setup_logger):
    """Test Access Legal Help Page."""
    logger = setup_logger("test_access_legal_help")
    try:
        response = client.get("/legal/help", follow_redirects=True)
        assert response.status_code == HTTPStatus.OK
        final_template_rendered = len(capture_templates) - 1
        assert capture_templates[final_template_rendered][0].name == "help.html"
        logger.info("Legal Help page rendered correctly.")
    except AssertionError as e:
        logger.error(f"Test failed: {str(e)}")
        raise


def test_access_legal_work_rights(client, capture_templates, setup_logger):
    """Test Access Workers' Rights Page."""
    logger = setup_logger("test_access_legal_work_rights")
    try:
        response = client.get("/legal/work_rights", follow_redirects=True)
        assert response.status_code == HTTPStatus.OK
        final_template_rendered = len(capture_templates) - 1
        assert (
            capture_templates[final_template_rendered][0].name
            == "work_rights.html"
        )
        logger.info("Workers' Rights page rendered correctly.")
    except AssertionError as e:
        logger.error(f"Test failed: {str(e)}")
        raise


def test_access_legal_renters_rights(client, capture_templates, setup_logger):
    """Test Access Renters' Rights Page."""
    logger = setup_logger("test_access_legal_renters_rights")
    try:
        response = client.get("/legal/renters_rights", follow_redirects=True)
        assert response.status_code == HTTPStatus.OK
        final_template_rendered = len(capture_templates) - 1
        assert (
            capture_templates[final_template_rendered][0].name
            == "renters_rights.html"
        )
        logger.info("Renters' Rights page rendered correctly.")
    except AssertionError as e:
        logger.error(f"Test failed: {str(e)}")
        raise


def test_access_legal_general(client, capture_templates, setup_logger):
    """Test Access General Legal Info Page."""
    logger = setup_logger("test_access_legal_general")
    try:
        response = client.get("/legal/general", follow_redirects=True)
        assert response.status_code == HTTPStatus.OK
        final_template_rendered = len(capture_templates) - 1
        assert (
            capture_templates[final_template_rendered][0].name == "general.html"
        )
        logger.info("General Legal Info page rendered correctly.")
    except AssertionError as e:
        logger.error(f"Test failed: {str(e)}")
        raise
