import sys
import subprocess

from importlib import import_module

from . import constants
from .utils import get_base_dir
from .http.server import HTTPRequestHandler, HTTPServer


class WebApp:
    def __init__(self):
        self.host = None
        self.port = None
        self.reg_sys_paths()

    def reg_sys_paths(self):
        """
        Registers the base directory of the application to the system path.
        Appends the application's base directory, as returned by get_base_dir(), to sys.path to ensure modules can be imported properly.
        """

        sys.path.append(get_base_dir())

    def run(self, host=None, port=None, reload=False):
        """
        Starts the web server with optional auto-reload support.
        Args:
            host (str, optional): The hostname to listen on. Defaults to a constant value.
            port (int, optional): The port to listen on. Defaults to a constant value.
            reload (bool, optional): If True, enables auto-reload on code changes.
        Handles graceful shutdown on keyboard interrupt.
        """

        self.host = host or constants.DEFAULT_HOST
        self.port = port or constants.DEFAULT_PORT

        if reload and not "--noreload" in sys.argv:
            print("🔁 Running with auto-reload...")
            try:
                subprocess.run(
                    [sys.executable, "framework/watcher.py", str(get_base_dir())]
                )
            except KeyboardInterrupt:
                pass

            return

        try:
            with HTTPServer((self.host, self.port), HTTPRequestHandler) as server:
                print(f"🚀 Server running at http://{self.host}:{self.port}")
                server.serve_forever()

        except KeyboardInterrupt:
            print("\n🛑 Server stopped.")

    def modules(self, module_list):
        """
        Dynamically imports the specified modules and their 'routes' submodules.
        """

        for module in module_list:
            try:
                import_module(module)
                import_module(f"{module}.routes")
            except ImportError as e:
                print(f"❌ Error loading module '{module}': {e}")
