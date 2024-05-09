import pytest
from flask import session
from werkzeug.datastructures import MultiDict
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired

# Define a simple form for testing
class SimpleForm(FlaskForm):
    field = StringField('Field', validators=[DataRequired()])

def test_form_rejection_without_csrf(client):
    """Test that the form rejects a submission without a CSRF token."""
    form = SimpleForm(formdata=MultiDict([('field', 'test')]), csrf_enabled=True)
    response = client.post('/submit_form', data=form.get_data(), follow_redirects=True)
    assert 'The CSRF token is missing.' in response.data.decode(), "CSRF protection is not functioning."

def test_form_acceptance_with_csrf(client, app):
    """Test that the form accepts a submission with a valid CSRF token."""
    with app.test_client() as client:
        with client.session_transaction() as sess:
            sess['csrf_token'] = 'test_csrf_token'
        form = SimpleForm(formdata=MultiDict([('field', 'test'), ('csrf_token', sess['csrf_token'])]), csrf_enabled=True)
        response = client.post('/submit_form', data=form.get_data(), follow_redirects=True)
        assert response.status_code == 200, "Form submission failed even with valid CSRF token."
