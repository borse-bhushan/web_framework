from framework.route import register_routes

from .handler import create_user, get_user_obj, get_all_user, update_user, delete_user


register_routes(route="/user", handler_func=create_user, http_methods=["POST"])
register_routes(route="/user", handler_func=get_all_user, http_methods=["GET"])
register_routes(
    route="/user/<str:user_id>", handler_func=get_user_obj, http_methods=["GET"]
)
register_routes(
    route="/user/<str:user_id>", handler_func=update_user, http_methods=["PUT"]
)
register_routes(
    route="/user/<str:user_id>", handler_func=delete_user, http_methods=["DELETE"]
)
