class Request:
    """Represents an HTTP request."""

    def __init__(self, method: str, url: str, headers: dict = None, body: str = None):

        self.url = url
        self.body = body
        self.method = method
        self.headers = headers if headers is not None else {}

    def get_header(self, name: str) -> str:
        """Retrieve a header value by its name."""
        return self.headers.get(name)

    def set_header(self, name: str, value: str):
        """Set a header value by its name."""
        self.headers[name] = value

    def __str__(self):
        return f"Request(method={self.method}, url={self.url}, headers={self.headers}, body={self.body})"
