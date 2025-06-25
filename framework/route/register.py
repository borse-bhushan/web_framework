class RouteRegistry:

    def __init__(self):
        self.routes = []

    def register(self, route, handler_func):
        """Register a route with its corresponding handler function."""
        self.routes.append({"route": route, "handler_func": handler_func})

    def find_handler(self, route):
        """Retrieve the handler function for a given route."""

        for r in self.routes:
            if r["route"] == route:
                return r["handler_func"]

        return None


route_registry = RouteRegistry()


def register_routes(route, handler_func):
    """
    Register a route with its corresponding handler function.
    """
    route_registry.register(route=route, handler_func=handler_func)


def get_handler(route):
    """
    Retrieve the handler function for a given route.
    :param route: The route to find the handler for.
    :return: The handler function if found, otherwise None.
    """
    return route_registry.find_handler(route)
