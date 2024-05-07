import sys
sys.path.append("/home/aishni.narain@intelegencia.com/Desktop/Library System Api/Library-Management-System-Api/app")

import datetime
import pytest
from unittest.mock import MagicMock,patch
from app import app as flask_app,db,pymysql
from flask_jwt_extended import jwt_required,create_access_token



SECRET_KEY = 'your_secret_key'

@pytest.fixture()
def app():
    app = flask_app
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://username:password@localhost/database'
    
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()
    
@pytest.fixture()
def client(app):
    return app.test_client()


# @pytest.fixture()
# def data():
#     return {'username_or_email': 'test@example.com'}

# @pytest.fixture
# def mock_jwt_required():
#     with patch('project.middleware.jwt_required') as mock_jwt:
#         yield mock_jwt


# @pytest.fixture
# def valid_authorization_header():
#     # Fixture to provide a valid authorization header with a valid access token
#     identity = 'test@example.com'
#     access_token = create_access_token(identity=identity, expires_delta=datetime.timedelta(hours=1))
#     return {'Authorization': f'Bearer {access_token}'}

# @pytest.fixture
# def invalid_authorization_header():
#     # Fixture to provide an invalid authorization header with an expired access token
#     identity = 'test@example.com'
#     access_token = create_access_token(identity=identity, expires_delta=datetime.timedelta(hours=-1))  # Token expired
#     return {'Authorization': f'Bearer {access_token}'}

# @pytest.fixture()
# def authorization_header():
#     identity = 'test@example.com'
#     access_token = create_access_token(identity=identity,expires_delta=datetime.timedelta(hours=1))
    
#     return {'Authorization': f'Bearer {access_token}'}

# @pytest.fixture
# def mock_access_required():
#     with patch('project.middleware.access_required') as mock_access:
#         yield mock_access
        
# @pytest.fixture
# def mock_dbsession():
#     return MagicMock()

# @pytest.fixture
# def mock_user():
#     return MagicMock()