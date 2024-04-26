import pytest
from bs4 import BeautifulSoup
from new_arrivals_chi.app.main import app

class TestBase:
    """Base class for test cases."""

    @pytest.fixture(autouse=True)
    def setup_client(self):
        """Fixture to setup Flask test client."""
        app.config["TESTING"] = True
        with app.test_client() as client:
            self.client = client
            yield client

    def get_page(self, url):
        """Perform a GET request and decode the response."""
        response = self.client.get(url)
        assert response.status_code == 200
        return response.data.decode('utf-8')

    def check_content(self, html_content, *strings):
        """Check multiple strings in HTML content."""
        for string in strings:
            assert string in html_content

    def find_buttons(self, html_content, *button_texts):
        """Check for the presence of buttons on a page."""
        soup = BeautifulSoup(html_content, 'html.parser')
        for text in button_texts:
            assert soup.find("button", string=text) is not None, f"{text} button not found"
