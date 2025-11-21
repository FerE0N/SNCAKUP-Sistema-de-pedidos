from .i_order_repository import IOrderRepository
from services.mongo_connection import MongoConnection

class MongoOrderRepository(IOrderRepository):
    """
    Repository Pattern (Data Access).
    Implementation for MongoDB.
    """
    def __init__(self):
        self.db = MongoConnection().db
        self.collection = self.db["orders"]

    def load_all(self):
        """Loads all orders from MongoDB."""
        # Convert ObjectId to string for JSON serialization if needed, 
        # but for now we just return the list of dicts.
        orders = list(self.collection.find({}, {"_id": 0}))
        return orders

    def save_all(self, orders):
        """
        In a real DB scenario, we wouldn't 'save_all' overwriting everything.
        But to keep the interface consistent with the previous JSON approach:
        We will just insert the *newest* order if we change the logic in Controller,
        OR we can clear and insert all (inefficient but matches interface).
        
        BETTER APPROACH for DB: The interface should probably have 'save(order)'.
        However, to strictly follow the existing interface without breaking changes yet:
        We will assume 'orders' contains ALL orders, but we only want to save the new ones.
        
        Actually, let's refactor the Controller to call a new method `save(order)` 
        if we were free to change the interface. 
        Since we must adhere to `IOrderRepository` which has `save_all(orders)`,
        we will implement a smart save or just insert the last one.
        
        Wait, the Controller logic is:
        orders = repo.load_all()
        orders.append(new_order)
        repo.save_all(orders)
        
        For MongoDB, this is bad. 
        Let's change the implementation to only insert the *last* order in the list 
        if it doesn't exist, or just wipe and recreate (easiest for "save_all" semantics).
        
        For this exercise, let's do the "Wipe and Replace" to be 100% consistent 
        with the JSON behavior, although it's not production-ready for huge data.
        """
        self.collection.delete_many({})
        if orders:
            self.collection.insert_many(orders)

    def save(self, order):
        """
        Extended method for better performance, if we update the controller.
        """
        self.collection.insert_one(order)
