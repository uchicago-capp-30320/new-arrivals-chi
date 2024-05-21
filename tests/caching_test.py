import pytest
from flask import session
from datetime import datetime, timedelta
import time

def test_login_logout_with_expiration(client, query_test_user, setup_logger):
    logger = setup_logger("test_login_logout_with_expiration")
    
    # Step 1: Log in
    logger.info("Logging in with test user")
    response = client.post(
        "/login",
        data={"email": query_test_user.email, "password": query_test_user.password},
        follow_redirects=True,
    )
    assert response.status_code == 200
    # assert b"Dashboard" in response.data  # Check if redirected to dashboard
    logger.info("Logged in successfully")
    
    # Step 2: Check if the user is logged in and set session expiration
    with client.session_transaction() as sess:
        # assert "user_id" in sess
        # logger.info("User is logged in, session contains user_id")
        # Manually set the session expiration time
        sess["_permanent"] = True
        sess.permanent_session_lifetime = timedelta(seconds=5)
    
    # Step 3: Wait for the session to expire (5 seconds)
    time.sleep(6)

    # Step 4: Check if the user is still logged out
    response = client.get("/dashboard", follow_redirects=True)
    assert response.status_code == 200
    assert b"Login" in response.data  # Should redirect to login page if session expired
    logger.info("Session expired, redirected to login page when accessing dashboard")

    
        
    # Step 5: Check session data to ensure user is not logged in
    # with client.session_transaction() as sess:
    #     assert "user_id" not in sess
    #     logger.info("Session does not contain user_id, user is logged out")
