from .handler import ProductHandler


ProductHandler.register_routes(
    "/product",
    {
        "post": "create_product",
        "put": "update_product",
        "delete": "delete_product",
        "get": ["get_product_obj", "get_all_products"],
        "details": ["get_product_obj", "update_product", "delete_product"],
    },
)
