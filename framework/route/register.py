from ..constants import METHOD_LIST


class RouteRegistry:

    def __init__(self):
        self.routes = []

    def register(self, route, handler_func, http_methods):
        """Register a route with its corresponding handler function."""
        self.routes.append(
            {
                "route": route,
                "handler_func": handler_func,
                "http_methods": http_methods,
            }
        )

    def find_handler(self, route, method):
        """Retrieve the handler function for a given route."""

        for r in self.routes:
            if r["route"] == route and method in r["http_methods"]:
                return r["handler_func"]

        return None


route_registry = RouteRegistry()


def register_routes(route, handler_func, http_methods=METHOD_LIST):
    """
    Register a route with its corresponding handler function.
    """

    if not http_methods:
        raise ValueError("HTTP methods list cannot be empty when registering a route.")

    if isinstance(http_methods, str):
        http_methods = [http_methods]

    route_registry.register(
        route=route, handler_func=handler_func, http_methods=http_methods
    )


def get_handler(route, method):
    """
    Retrieve the handler function for a given route.
    :param route: The route to find the handler for.
    :return: The handler function if found, otherwise None.
    """
    return route_registry.find_handler(route, method)
