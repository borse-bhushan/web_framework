from framework.route import register_routes

from .handler import create_user


register_routes(route="/user", handler_func=create_user, http_methods=None)
