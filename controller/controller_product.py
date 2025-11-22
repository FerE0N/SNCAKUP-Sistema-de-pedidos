# controller/controller_product.py
from model.factories import ProductFactory

class ControllerProduct:
    def get_all_products(self):
        # Simulación de base de datos de productos
        # Ahora incluimos URLs de imágenes (placeholders atractivos)
        return [
            ProductFactory.create_product("food", "Tacos", 15.0, "https://images.unsplash.com/photo-1551504734-5ee1c4a1479b?auto=format&fit=crop&w=400&q=80"),
            ProductFactory.create_product("food", "Pizza", 20.0, "https://images.unsplash.com/photo-1513104890138-7c749659a591?auto=format&fit=crop&w=400&q=80"),
            ProductFactory.create_product("drink", "Refresco", 10.0, "https://images.unsplash.com/photo-1622483767028-3f66f32aef97?auto=format&fit=crop&w=400&q=80"),
            ProductFactory.create_product("drink", "Agua", 8.0, "https://images.unsplash.com/photo-1548839140-29a749e1cf4d?auto=format&fit=crop&w=400&q=80"),
            ProductFactory.create_product("food", "Hamburguesa", 45.0, "https://images.unsplash.com/photo-1568901346375-23c9450c58cd?auto=format&fit=crop&w=400&q=80"),
            ProductFactory.create_product("food", "Hot Dog", 25.0, "https://images.unsplash.com/photo-1612392062631-94dd858cba88?auto=format&fit=crop&w=400&q=80")
        ]
