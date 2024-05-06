import pytest
from ..app import app as flask_app,db

@pytest.fixture()
def app():
    app = flask_app
    app.config['TESTING'] = True 
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://username:password@localhost/db_name'
    
    with app.app_context():
        db.create_all()
        yield app
    
@pytest.fixture()
def client(app):
    return app.test_client()