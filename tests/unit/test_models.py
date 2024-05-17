from models import Role

def test_new_role():
    role = Role(1,"Admin")
    assert role.id == 1
    assert role.role_name == "Admin"