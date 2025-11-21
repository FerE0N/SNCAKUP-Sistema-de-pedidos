from pymongo import MongoClient

class MongoConnection:
    """
    Singleton Pattern (Creational).
    Manages the connection to the MongoDB database.
    """
    _instance = None
    _client = None
    _db = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MongoConnection, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        # Assuming local MongoDB instance 
        self._client = MongoClient("mongodb://localhost:27017/")
        self._db = self._client["snackup_db"]
        print("[MongoConnection] Connected to MongoDB: snackup_db")

    @property
    def db(self):
        return self._db
