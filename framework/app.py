import sys

from importlib import import_module

from . import constants
from .utils import get_base_dir
from .http.server import HTTPRequestHandler, HTTPServer


class WebApp:

    def __init__(self, host=constants.DEFAULT_HOST, port=constants.DEFAULT_PORT):

        self.host = host
        self.port = port

        self.reg_sys_paths()

    def reg_sys_paths(self):
        """
        Register system paths for the application.
        This method can be used to add additional directories to the Python path.
        """

        sys.path.append(get_base_dir())

    def run(self):
        """Start the web application server."""
        try:
            with HTTPServer((self.host, self.port), HTTPRequestHandler) as server:
                print(f"🚀 Server running at http://{self.host}:{self.port}")
                server.serve_forever()

        except KeyboardInterrupt:
            print("\n🛑 Server stopped.")

    def modules(self, module_list):
        """
        Load modules into the application.
        :param module_list: List of module names to load.
        """

        for module in module_list:
            try:
                imp_module = import_module(module)
                if imp_module:
                    import_module(f"{module}.routes")

            except ImportError as e:
                print(f"❌ Error loading module '{module}': {e}")
