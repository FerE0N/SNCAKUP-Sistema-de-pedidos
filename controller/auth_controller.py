from repository.mongo_user_repository import MongoUserRepository
from model.user import User

class AuthController:
    """
    Controller for Authentication logic.
    """
    def __init__(self):
        self.repo = MongoUserRepository()

    def login(self, username, password):
        user = self.repo.find_by_username(username)
        if user and user.password == password:
            return True
        return False

    def register(self, username, password):
        user = User(username, password)
        return self.repo.create_user(user)
