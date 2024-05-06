def get_access_token(client):
    login_data = {
        'username_or_email':'valid_username_or_email',
        'password': 'valid_password'
    }
    url = '/api/v1/users/login'
    response = client.post(url, json= login_data)
    json_response = response.get_json()
    
    return json_response['token']['access_token']

    
def test_login_successful(client):
    valid_data = {
        'username_or_email':'valid_username_or_email',
        'password': 'valid_password'
    }
    url = '/api/v1/users/login'
    response = client.post(url, json= valid_data)
    json_response = response.get_json()
    
    
    assert response.status_code == 200
    assert json_response['msg'] == 'Logged in Successfully!'
    assert 'token' in json_response

def test_register_user(client):
    
    access_token = test_login_successful(client)
    print(access_token)
    # Test registering a user with valid data
    valid_data = {
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'testpassword'
    }
    
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    
    response = client.post('/api/v1/users/register', json=valid_data, headers=headers)
    # assert response.status_code == 200
    print(response.json)
    # assert 'msg' in response.json
    # assert 'Signup Successful! User Created Successfully!' in response.json['msg']