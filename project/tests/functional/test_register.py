from project.models import User
import json
from pytest_mock import mocker

def test_register_user_success(client,mocker):
    mock_data = {
        "username":"testuser",
        "email":"test@email.com",
        "password":"testpassword"
    }
    
    mocker.patch('flask.request.get_json', return_value=mock_data)

    # Mocking database operations
    mocker.patch('your_flask_app.User.query.filter_by', side_effect=[None, None])
    mocker.patch('your_flask_app.db.session.add')
    mocker.patch('your_flask_app.db.session.commit')

    
    response = client.post('/users/register',json= mock_data)
    assert response.status_code == 200