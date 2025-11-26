from model.factories import ProductFactory
from services.mongo_connection import MongoConnection

class ControllerProduct:
    def __init__(self):
        self.db = MongoConnection().db
        self.collection = self.db["products"]

    def get_all_products(self):
        """Fetches all products from MongoDB and converts them to Product objects."""
        product_docs = self.collection.find()
        products = []
        
        for doc in product_docs:
            # Factory expects: type, name, price, image_url
            # We stored 'type' in the seed script ('food' or 'drink')
            p_type = doc.get("type", "food") 
            name = doc.get("name")
            price = doc.get("price")
            image_url = doc.get("image_url")
            
            product = ProductFactory.create_product(p_type, name, price, image_url)
            products.append(product)
            
        return products
