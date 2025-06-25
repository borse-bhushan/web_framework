from framework.route import register_routes

from .handler import hello_world


register_routes(route="/hello", handler_func=hello_world)

print("Routes registered in user module.")
