import socketserver

from ..route import get_handler

from .request import Request


class HTTPRequestHandler(socketserver.BaseRequestHandler):
    routes = {}

    def recv_all(self, buffer_size=1024):
        """Receive data from the socket."""
        buffer = b""
        while b"\r\n\r\n" not in buffer:
            data = self.request.recv(buffer_size)
            if not data:
                break
            buffer += data

        headers = buffer.decode("utf-8", errors="replace")
        content_length = 0

        for line in headers.split("\r\n"):
            if line.lower().startswith("content-length:"):
                content_length = int(line.split(":")[1].strip())

        body_bytes = b""
        while len(body_bytes) < content_length:
            body_bytes += self.request.recv(buffer_size)

        return headers + body_bytes.decode("utf-8", errors="replace")

    def dispatch_request(self, request: Request):
        """Dispatch the request to the appropriate handler."""
        handler = get_handler(request.url)

        if callable(handler):
            return handler(request)

        return "Hello"

    def handle(self):
        data = self.recv_all()
        if not data:
            return

        lines = data.splitlines()
        request_line = lines[0]
        method, path, _ = request_line.split()

        request = Request(
            method=method,
            url=path,
            headers={
                line.split(": ")[0]: line.split(": ")[1]
                for line in lines[1:]
                if ": " in line
            },
            body=data.split("\r\n\r\n", 1)[1] if "\r\n\r\n" in data else "",
        )

        response = self.dispatch_request(request)

        # HTTP Response
        response = (
            "HTTP/1.1 200 OK\r\n"
            "Content-Type: text/plain\r\n"
            f"Content-Length: {len(response)}\r\n"
            "\r\n"
            f"{response}"
        )
        self.request.sendall(response.encode())

    @classmethod
    def route(cls, path, method="GET"):
        def decorator(func):
            cls.routes[(method.upper(), path)] = func
            return func

        return decorator

    def not_found(self):
        return "404 Not Found"


class HTTPServer(socketserver.ThreadingTCPServer):
    allow_reuse_address = True
