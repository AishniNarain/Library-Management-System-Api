import json
def test_login(client):
    valid_data = {
        'username_or_email':'valid_username_or_email',
        'password': 'testpassword'
    }
    url = '/api/v1/users/login'
    response = client.post(url, json= valid_data)
    print(response.json)
    
    # data = json.loads(response.data)
    
    assert response.status_code == 200
    # assert data['message'] == 'Logged in Successfully!'
    # print(response.json)
    # return response.json['token']


# def test_register_user(client):
    
#     access_token = get_access_token(client)
#     # Test registering a user with valid data
#     valid_data = {
#         'username': 'test_user',
#         'email': 'test@example.com',
#         'password': 'test_password'
#     }
    
#     headers = {'Authorization': f'Bearer {access_token}'}
#     response = client.post('/api/v1/users/register', json=valid_data, headers=headers)
#     assert response.status_code == 200
#     print(response.json)
#     assert 'msg' in response.json
    # assert 'Signup Successful! User Created Successfully!' in response.json['msg']