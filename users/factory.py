from users.service import Users

class UsersFactory:
    
    @staticmethod
    def create_users():
        return Users.create()