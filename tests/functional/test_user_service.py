import json
from unittest.mock import patch, MagicMock
from flask_jwt_extended import jwt_required

def test_login_successful(client):
    valid_data = {
        'username_or_email':'valid_username_or_email',
        'password': 'valid_password'
    }
    url = '/api/v1/users/login'
    response = client.post(url, json= valid_data)
    # json_response = response.get_json()

    assert response.status_code == 200
    # assert json_response['msg'] == 'Logged in Successfully!'
    # assert 'token' in json_response

# def test_register_user(client, authorization_header,mock_access_required):
    
#     mock_access_required.return_value = (['Admin','Librarian'],['1'])
    
#     # mock_user.username = 'existinguser'
#     # mock_dbsession.query().filter_by().first.return_value = mock_user
    
#     url = '/api/v1/users/register'
    
#     valid_data = {
#         'username': 'testuser',
#         'email': 'test@example.com',
#         'password': 'test_password'
#     }

#     response = client.post(url, json=valid_data, headers= authorization_header)
#     print(response)
    # assert response.status_code == 200
    # print(response.json)
    # assert 'msg' in response.json
    # assert 'Signup Successful! User Created Successfully!' in response.json['msg']
    
    
# def test_access_granted(client, authorization_header, mock_access_required):
#     # Test case where access is granted based on required roles and permissions
#     mock_access_required.return_value = (['Admin'], ['1'])
    
#     data = {
#         'username': 'testuser',
#         'email': 'test@example.com',
#         'password': 'testpassword'
#     }
#     response = client.post('/api/v1/users/register',json=data, headers=authorization_header)
#     # assert response.status_code == 200  # Ensure access is granted
#     print(response)
    
# def test_access_denied(client, valid_authorization_header, mock_access_required):
#     # Test case where access is denied due to insufficient roles or permissions
#     data = {
#         'username': 'testuser',
#         'email': 'test@example.com',
#         'password': 'test_password'
#     }
#     mock_access_required.return_value = (['User'], ['1'])
#     response = client.post('/api/v1/users/register', json=data,headers=valid_authorization_header)
#     print(response)
    # assert response.status_code == 403  # Ensure access is denied

# def test_invalid_token(client, invalid_authorization_header, mock_access_required):
#     # Test case where access is denied due to an invalid token
#     data = {
#         'username': 'testuser',
#         'email': 'test@example.com',
#         'password': 'test_password'
#     }
#     mock_access_required.return_value = (['Admin'], ['1'])
#     response = client.post('/api/v1/users/register',json=data, headers=invalid_authorization_header)
#     assert response.status_code == 401  # Ensure access is denied due to invalid token