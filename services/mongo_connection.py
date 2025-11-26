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
        # MongoDB Atlas Connection
        username = "falcnss21_db_user"
        password = "K8RdgJ6Rujx1WqB0"
        cluster_url = "cluster0.zlirjz3.mongodb.net"
        
        uri = f"mongodb+srv://{username}:{password}@{cluster_url}/?retryWrites=true&w=majority&appName=Cluster0"
        try:
            self._client = MongoClient(uri)
            # Trigger a connection check
            self._client.admin.command('ping')
            print(f"[MongoConnection] ✅ Connected to MongoDB Atlas: {cluster_url}")
        except Exception as e:
            print(f"[MongoConnection] ❌ Failed to connect to Atlas: {e}")
            print("   Using localhost as fallback...")
            self._client = MongoClient("mongodb://localhost:27017/")
            
        self._db = self._client["snackup_db"]

    @property
    def db(self):
        return self._db
