from ...models import User

def test_new_user():
    user = User(username ='testusername', email = 'test@email.com')
    assert user.username == 'testusername'
    assert user.email == 'test@email.com'