from services.mongo_connection import MongoConnection
from model.user import User

class MongoUserRepository:
    """
    Repository for User management in MongoDB.
    """
    def __init__(self):
        self.db = MongoConnection().db
        self.collection = self.db["users"]

    def create_user(self, user: User):
        if self.find_by_username(user.username):
            return False # User already exists
        
        self.collection.insert_one({
            "username": user.username,
            "password": user.password # In real app, hash this!
        })
        return True

    def find_by_username(self, username: str) -> User:
        data = self.collection.find_one({"username": username})
        if data:
            return User(data["username"], data["password"])
        return None
