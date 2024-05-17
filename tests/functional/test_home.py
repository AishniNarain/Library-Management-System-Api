from app import app
import os

def test_home_page():
    os.environ['CONFIG_TYPE'] = 'config.TestingConfig'
    flask_app = app

    # Create a test client using the Flask application configured for testing
    with flask_app.test_client() as test_client:
        response = test_client.get('/')
        assert response.status_code == 200