from base_test import TestBase


class TestHomePage(TestBase):
    """Tests functionality on the home page"""

    def test_home_page_content(self):
        """Test the static content and language-specific content"""
        html_content = self.get_page("/")
        self.check_content(
            html_content,
            "Welcome",
            "Find essential support for legal, health, and food needs.",
            "Please click below to begin:",
        )

        html_content = self.get_page("/?lang=es")
        self.check_content(
            html_content,
            "Bienvenido",
            "Encuentra apoyo para tus necesidades legales, "
            "de salud o de comida.",
            "Por favor haz click abajo para comenzar:",
        )

    def test_navigation_bar(self):
        """Verify that the navigation bar contains all required links"""
        html_content = self.get_page("/")
        self.check_content(
            html_content, "<nav", "Home", "Profile", "Legal", "Login", "Sign Up"
        )

    def test_buttons(self):
        """Verify that all necessary buttons are present on the home page"""
        html_content = self.get_page("/")
        self.find_buttons(html_content, "Legal", "Health", "Food")

    def test_button_links(self):
        """Test that buttons link correctly in English/Spanish"""
        html_content = self.get_page("/")
        self.check_content(
            html_content,
            "navigateTo('/legal', 'en')",
            "window.location.href='/health'",
            "window.location.href='/food'",
        )

        html_content = self.get_page("/?lang=es")
        self.check_content(
            html_content,
            "navigateTo('/legal', 'es')",
            "window.location.href='/health'",
            "window.location.href='/food'",
        )
