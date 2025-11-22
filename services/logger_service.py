from services.mongo_connection import MongoConnection
import datetime

class LoggerService:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(LoggerService, cls).__new__(cls)
            cls._instance.db = MongoConnection().db
            cls._instance.collection = cls._instance.db["logs"]
        return cls._instance

    def log(self, level, message, user=None, details=None):
        """
        Registra un evento en la base de datos.
        """
        log_entry = {
            "timestamp": datetime.datetime.now(),
            "level": level, # INFO, WARNING, ERROR
            "message": message,
            "user": user or "Anonymous",
            "details": details or {}
        }
        try:
            self.collection.insert_one(log_entry)
            print(f"[LOG-{level}] {message}") 
        except Exception as e:
            print(f"CRITICAL: FAILED TO LOG TO DB: {e}")

    def info(self, message, user=None, details=None):
        self.log("INFO", message, user, details)

    def warning(self, message, user=None, details=None):
        self.log("WARNING", message, user, details)

    def error(self, message, user=None, details=None):
        self.log("ERROR", message, user, details)
