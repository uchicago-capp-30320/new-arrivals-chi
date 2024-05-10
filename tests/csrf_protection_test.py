from bs4 import BeautifulSoup


def get_csrf_token_from_response(html):
    """Parses CSRF token from HTML response."""
    soup = BeautifulSoup(html, "html.parser")
    token = soup.find("input", {"name": "csrf_token"})["value"]
    return token


def test_login_form_rejection_without_csrf(client):
    """Ensure the login form rejects a submission without a CSRF token."""
    response = client.post(
        "/login",
        data={"email": "user@example.com", "password": "securepassword"},
        follow_redirects=True,
    )
    assert (
        "The CSRF token is missing." in response.data.decode()
        or response.status_code == 400
    ), "Form should reject submission without CSRF token"


def test_login_form_acceptance_with_csrf(client, app):
    """Ensure the login form accepts a submission with a valid CSRF token."""
    # Get the login page to retrieve the CSRF token
    response = client.get("/login")
    csrf_token = get_csrf_token_from_response(response.data.decode())

    # Submit the form with CSRF token
    response = client.post(
        "/login",
        data={
            "email": "user@example.com",
            "password": "Str0ngP@$$word123!C0ntre$namUyfue&t3",
            "csrf_token": csrf_token,
        },
        follow_redirects=True,
    )
    assert (
        response.status_code == 200
    ), "Form should accept submission with valid CSRF token"


def test_login_post_invalid_csrf(client):
    """Ensure the login form rejects a submission with an invalid CSRF token."""
    response = client.post(
        "/login",
        data={
            "email": "test@example.com",
            "password": "TestP@ssword!4234m!@3",
            "csrf_token": "invalid_csrf_token",
        },
        follow_redirects=True,
    )
    assert (
        "Invalid CSRF token. Please try again." in response.data.decode()
        or response.status_code == 400
    ), "Form should reject submission with invalid CSRF token"


def test_login_post_valid_csrf(client, test_user):
    """Ensure the login form accepts a submission with a valid CSRF token."""
    response = client.get("/login")
    csrf_token = get_csrf_token_from_response(response.data.decode())

    response = client.post(
        "/login",
        data={
            "email": "test@example.com",
            "password": "TestP@ss3fsadf3!@!@#",
            "csrf_token": csrf_token,
        },
        follow_redirects=True,
    )
    assert (
        response.status_code == 200
    ), "Form should accept submission with valid CSRF token"


def test_signup_form_rejection_without_csrf(client):
    """Ensure the signup form rejects a submission without a CSRF token."""
    response = client.post(
        "/signup",
        data={
            "email": "test@example.com",
            "password": "TestP@ss35!@!@#daf3",
            "password_confirm": "TestP@ss35!@!@#daf3",
        },
        follow_redirects=True,
    )
    assert (
        "The CSRF token is missing." in response.data.decode()
        or response.status_code == 400
    ), "Form should reject submission without CSRF token"


def test_signup_form_acceptance_with_csrf(client):
    """Ensure the signup form accepts a submission with a valid CSRF token."""
    response = client.get("/signup")
    csrf_token = get_csrf_token_from_response(response.data.decode())

    response = client.post(
        "/signup",
        data={
            "email": "test@example.com",
            "password": "TestP@ss35!@!@#daf3",
            "password_confirm": "TestP@ss35!@!@#daf3",
            "csrf_token": csrf_token,
        },
        follow_redirects=True,
    )
    assert (
        response.status_code == 200
    ), "Form should accept submission with valid CSRF token"


def test_signup_post_invalid_csrf(client):
    """Ensure the signup form rejects a submission with an invalid CSRF token."""
    response = client.post(
        "/signup",
        data={
            "email": "test@example.com",
            "password": "T$R%#@$FASD3m2o3sdf",
            "password_confirm": "T$R%#@$FASD3m2o3sdf",
            "csrf_token": "invalid_csrf_token",
        },
        follow_redirects=True,
    )
    assert (
        "Invalid CSRF token. Please try again." in response.data.decode()
        or response.status_code == 400
    ), "Form should reject submission with invalid CSRF token"


def test_signup_post_valid_csrf(client):
    """Ensure the signup form accepts a submission with a valid CSRF token."""
    response = client.get("/signup")
    csrf_token = get_csrf_token_from_response(response.data.decode())

    response = client.post(
        "/signup",
        data={
            "email": "test@example.com",
            "password": "T$R%#@$3o2m3v23lkmasdf",
            "password_confirm": "T$R%#@$3o2m3v23lkmasdf",
            "csrf_token": csrf_token,
        },
        follow_redirects=True,
    )


def test_change_password_form_rejection_without_csrf(client):
    """Ensure the change password form rejects a submission without a CSRF token."""
    response = client.post(
        "/change_password",
        data={
            "old_password": "TestingP@ss35",
            "new_password": "NewTestingPsdf23r55",
            "new_password_confirm": "TestP@NewTestingPsdf23r55",
        },
        follow_redirects=True,
    )
    assert (
        "The CSRF token is missing." in response.data.decode()
        or response.status_code == 400
    ), "Form should reject submission without CSRF token"


def test_change_password_form_acceptance_with_csrf(client):
    """Ensure the change password form accepts a submission with a valid CSRF token."""
    response = client.get("/change_password")
    csrf_token = get_csrf_token_from_response(response.data.decode())

    response = client.post(
        "/change_password",
        data={
            "old_password": "TestingP@ss35",
            "new_password": "NewTestingPsdf23r55",
            "new_password_confirm": "NewTestingPsdf23r55",
            "csrf_token": csrf_token,
        },
        follow_redirects=True,
    )
    assert (
        response.status_code == 200
    ), "Form should accept submission with valid CSRF token"


def test_change_password_post_invalid_csrf(client):
    """Ensure the change password form rejects a submission with an invalid CSRF token."""
    response = client.post(
        "/change_password",
        data={
            "old_password": "TestingP@ss35",
            "new_password": "NewTestingPsdf23r55",
            "new_password_confirm": "NewTestingPsdf23r55",
            "csrf_token": "invalid_csrf_token",
        },
        follow_redirects=True,
    )
    assert (
        "Invalid CSRF token. Please try again." in response.data.decode()
        or response.status_code == 400
    ), "Form should reject submission with invalid CSRF token"


def test_change_password_post_valid_csrf(client):
    """Ensure the change password form accepts a submission with a valid CSRF token."""
    response = client.get("/change_password")
    csrf_token = get_csrf_token_from_response(response.data.decode())

    response = client.post(
        "/change_password",
        data={
            "old_password": "TestingP@ss35",
            "new_password": "NewTestingPsdf23r55",
            "new_password_confirm": "NewTestingPsdf23r55",
            "csrf_token": csrf_token,
        },
        follow_redirects=True,
    )
    assert (
        response.status_code == 200
    ), "Form should accept submission with valid CSRF token"
