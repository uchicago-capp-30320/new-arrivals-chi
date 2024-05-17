from bs4 import BeautifulSoup

def get_csrf_token_from_response(html):
    """Parses the CSRF token from an HTML response.

    Args:
        html (str): The HTML content from which to parse the CSRF token.

    Returns:
        str: The CSRF token extracted from the HTML input.
    """
    soup = BeautifulSoup(html, "html.parser")
    token = soup.find("input", {"name": "csrf_token"})["value"]
    return token