from ..route import register_routes


class BaseAPIHandler:
    lookup_field = None
    _http_method_and_handler_func_name = None

    _handler_instance = None

    @classmethod
    def register_routes(cls, route: str, http_method_and_handler_func_name: dict):
        """
        Registers HTTP routes for the handler class.
        This method associates HTTP methods and their corresponding handler function names with a given route.
        It supports dynamic route generation based on the presence of a lookup field and detail routes.
        Args:
            route (str): The base URL route to register.
            http_method_and_handler_func_name (dict): A dictionary mapping HTTP methods (as keys) to handler function names (as values).
                An optional key "" (empty string) can be used to specify detail handler function names.
        Returns:
            bool: True if the routes were registered successfully.
        Notes:
            - If a lookup field is defined and detail handlers are specified, the route is extended with a dynamic segment.
            - For each HTTP method and handler function name, the corresponding handler function is retrieved from the handler instance and registered.
        """


        if cls._handler_instance is None:
            cls._handler_instance = cls()

        obj = cls._handler_instance

        d_route = route
        detail = http_method_and_handler_func_name.pop("details", [])

        if cls.lookup_field and detail:
            if detail and isinstance(detail, str):
                detail = [detail]

            d_route += f"/<str:{cls.lookup_field}>"

        for method, handler_function_names in http_method_and_handler_func_name.items():

            if isinstance(handler_function_names, str):
                handler_function_names = [handler_function_names]

            for handler_fun_name in handler_function_names:

                handler_func = getattr(obj, handler_fun_name)

                path = d_route if detail and handler_fun_name in detail else route

                register_routes(
                    route=path,
                    handler_func=handler_func,
                    http_methods=method.upper(),
                )

        return True
