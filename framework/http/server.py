import socketserver

from ..route import get_handler
from ..exceptions.exceptions import NotFoundException, ContentTypeException

from .request import Request
from .responses import JsonResponse, BaseResponse


class HTTPRequestHandler(socketserver.BaseRequestHandler):

    def recv_all(self, buffer_size=1024):
        """Receive data from the socket."""

        buffer = b""

        # Step 1: Read until we find the end of headers
        while b"\r\n\r\n" not in buffer:
            data = self.request.recv(buffer_size)
            if not data:
                break
            buffer += data

        # Split header and the beginning of the body
        header_part, _, body_start = buffer.partition(b"\r\n\r\n")

        headers_text = header_part.decode("utf-8", errors="replace")
        content_length = 0

        # Step 2: Extract Content-Length (if present)
        for line in headers_text.split("\r\n"):
            if line.lower().startswith("content-length:"):
                content_length = int(line.split(":", 1)[1].strip())

        # Step 3: Continue reading the body (if any)
        body_bytes = body_start
        while len(body_bytes) < content_length:
            chunk = self.request.recv(buffer_size)
            if not chunk:
                break
            body_bytes += chunk

        # Combine both parts
        full_request = header_part + b"\r\n\r\n" + body_bytes
        return full_request.decode("utf-8", errors="replace")


    def dispatch_request(self, request: Request):
        """Dispatch the request to the appropriate handler."""
        handler, path_params = get_handler(request.path, request.method)

        if callable(handler):
            return handler(request, **path_params)

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
