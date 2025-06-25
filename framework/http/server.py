import socketserver

from ..route import get_handler
from ..exceptions.exceptions import NotFoundException, ContentTypeException

from .request import Request
from .responses import JsonResponse, BaseResponse


class HTTPRequestHandler(socketserver.BaseRequestHandler):

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
        handler = get_handler(request.path, request.method)

        if callable(handler):
            return handler(request)

        raise NotFoundException()

    def generate_response(self, request: Request, response: BaseResponse):
        """Generate a response based on the request."""
        return response.to_response(request)

    def handle_request(self, request: Request):
        """Handle the request and return a response."""
        try:
            response = self.dispatch_request(request)
        except (NotFoundException, ContentTypeException) as e:
            response = JsonResponse(
                data={"error": e.message},
                status_code=e.status_code,
            )

        return self.generate_response(request, response)

    def handle(self):
        """Handle the incoming request."""

        data = self.recv_all()
        if not data:
            return

        request = Request()
        request.parse_request(data)

        response = self.handle_request(request)

        self.request.sendall(response.encode())

        return True


class HTTPServer(socketserver.ThreadingTCPServer):
    allow_reuse_address = True
