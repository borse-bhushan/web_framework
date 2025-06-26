import re

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
                "r_route": self._convert_path_to_regex(route),
            }
        )

    def find_handler(self, route, method):
        """Retrieve the handler function for a given route."""

        for r in self.routes:
            if method not in r["http_methods"]:
                continue

            match = re.match(r["r_route"], route)
            if not match:
                continue

            return r["handler_func"], match.groupdict()

        return None, {}

    def _convert_path_to_regex(self, path: str) -> str:
        # Replace <int:name> → (?P<name>\d+)
        path = re.sub(
            r"<int:([a-zA-Z_]+)>",
            lambda m: f"(?P<{m.group(1)}>\\d+)",
            path,
        )

        # Replace <str:name> → (?P<name>[^/]+)
        path = re.sub(
            r"<str:([a-zA-Z_]+)>",
            lambda m: f"(?P<{m.group(1)}>[^/]+)",
            path,
        )

        return f"^{path}$"


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
