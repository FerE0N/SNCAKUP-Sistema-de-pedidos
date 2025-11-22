from repository.mongo_user_repository import MongoUserRepository
from model.user import User
from services.logger_service import LoggerService

class AuthController:
    """
    Controller for Authentication logic.
    """
    def __init__(self):
        self.repo = MongoUserRepository()
        self.logger = LoggerService()

    def login(self, username, password):
        user = self.repo.find_by_username(username)
        if user and user.password == password:
            self.logger.info(f"User logged in: {username}", user=username)
            return True
        self.logger.warning(f"Failed login attempt for: {username}", user=username)
        return False

    def register(self, username, password):
        user = User(username, password)
        if self.repo.create_user(user):
            self.logger.info(f"New user registered: {username}", user=username)
            return True
        self.logger.warning(f"Registration failed (user exists): {username}", user=username)
        return False
