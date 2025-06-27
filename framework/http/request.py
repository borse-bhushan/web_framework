import json

from urllib.parse import urlparse, parse_qs

from ..exceptions.exceptions import ContentTypeException


class Request:
    """Represents an HTTP request."""

    def __init__(self):

        self.path = None
        self._body = None
        self.method = None
        self.r_path = None
        self.headers = None
        self.query_params = None
        self.http_version = None

    def parse_request(self, data):
        """
        Parses a raw HTTP request string and extracts its components.
        Args:
            data (str): The raw HTTP request as a string.
        Sets:
            self.method (str): The HTTP method (e.g., 'GET', 'POST').
            self.http_version (str): The HTTP version (e.g., 'HTTP/1.1').
            self.r_path (str): The original request path (may include query string).
            self.path (str): The URL path component (without query string).
            self.query_params (dict): Dictionary of query parameters parsed from the URL.
            self.headers (dict): Dictionary of HTTP headers.
            self._body (str or None): The request body, if present; otherwise None.
        Raises:
            ValueError: If the request line is malformed or missing required components.
        """

        lines = data.splitlines()
        request_line = lines[0]
        method, path, version = request_line.split()

        self.method = method.upper()
        self.http_version = version

        self.r_path = path
        parsed_url = urlparse(path)

        self.path = parsed_url.path
        self.query_params = parse_qs(parsed_url.query)

        self.headers = {
            line.split(": ")[0]: line.split(": ")[1]
            for line in lines[1:]
            if ": " in line
        }
        self._body = data.split("\r\n\r\n", 1)[1] if "\r\n\r\n" in data else None

    @property
    def body(self):
        """Return the body of the request."""
        content_type = self.headers.get("Content-Type", "application/json")

        if content_type != "application/json":
            raise ContentTypeException()

        return json.loads(self._body) if self._body else {}

    def __str__(self):
        return f"[Request] {self.method} {self.r_path}"
