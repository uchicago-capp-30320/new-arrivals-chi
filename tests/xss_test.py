"""Project: New Arrivals Chi.

File name: xxs_test.py

This test suite pressure tests the app for XSS attacks.

Methods:
    * test_xss_script_tag_injection

Last updated:
@Author: Kathryn Link-Oberstar @klinkoberstar
@Date: 05/09/2024

Creation:
@Author: Kathryn Link-Oberstar @klinkoberstar
@Date: 05/09/2024
"""
def test_xss_script_tag_injection(client):
    """""
    Test the resistance of the change password form to XSS attacks. 

    Attempt to inject a script tag into the new password fields. This test 
    ensures that script tags submitted through the change password form are 
    properly escaped or removed.
    """""
    response = client.post(
        "/change_password",
        data={
            "old_password": "validPassword1!",
            "new_password": "<script>alert('XSS');</script>",
            "new_password_confirm": "<script>alert('XSS');</script>"
        },
        follow_redirects=True
    )
    assert "<script>alert('XSS');</script>" not in response.data.decode()
    assert response.status_code == 200